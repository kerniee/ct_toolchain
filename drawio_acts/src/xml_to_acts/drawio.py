import logging
import xml.etree.ElementTree as ET

from pydrawio import decompress
from pydrawio.mxfile import Mxfile
from pydrawio.mxgraphmodel import MxGraphModel, MxCell

from xml_to_acts.acts import toACTS
from xml_to_acts.node import Node


class GraphException(Exception):
    pass


def hasattrs(obj, *attrs):
    return all(hasattr(obj, attr) for attr in attrs)


def is_edge(xml):
    return hasattrs(xml, "edge", "source", "target") and xml.edge


def is_node(xml):
    return hasattrs(xml, "value", "vertex") and xml.value


def create_graph(model: MxGraphModel) -> Node:
    nodes = {}
    edges = set()
    for xml in model.content.items:
        if not isinstance(xml, MxCell):
            continue
        if is_node(xml):
            nodes[xml.id] = Node.from_xml(xml)
        if is_edge(xml):
            edges.add((xml.source, xml.target))

    for source, target in edges:
        parent, child = nodes[source], nodes[target]
        if child.parent and child.parent != parent:
            raise GraphException(f"Multiple parents for node {child} found: {parent} and {child.parent}")
        child.parent = parent
        parent.children.append(child)

    root = None
    for node in nodes.values():
        if node.parent or not node.children:
            continue
        if root and root != node:
            raise GraphException(f"Multiple root nodes found: {root} and {node}")
        else:
            root = node
    return root


def model_from_xml(xml):
    tree = ET.ElementTree(ET.fromstring(xml))
    root = tree.getroot()
    diagram = root[0]
    model_xml = ET.tostring(diagram[0], encoding="unicode")
    return MxGraphModel(model_xml)


def xml_to_acts(xml: str, name: str = "Convertor result"):
    mx_file = Mxfile(xml)

    diagram = mx_file.diagram[0]
    if diagram.value.strip():
        mx_graph_model = decompress(diagram.value)
    else:
        mx_graph_model = model_from_xml(xml)

    root = create_graph(mx_graph_model)
    logging.debug("\n" + root.prettify())
    logging.debug(f"Classes: {' '.join(map(str, filter(Node.is_class, root.dfs())))}")
    return toACTS(root, name)
