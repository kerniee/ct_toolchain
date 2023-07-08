from collections import defaultdict
from dataclasses import dataclass, field
from os.path import splitext

from xml_to_acts.node import Node


@dataclass
class Section:
    name: str
    params: dict = field(default_factory=dict)

    def tostring(self):
        params = "\n".join(f"{k}: {v}" for k, v in sorted(self.params.items()))
        return f"[{self.name}]\n{params}"


def toACTS(root: Node, name: str):
    sections = []

    system = Section("System", {"Name": name})
    sections.append(system)

    params = defaultdict(list)
    for node in root.dfs():
        if node.is_class():
            key = f"{node.parent.value.strip()}(enum)"
            params[key].append(node.value.strip())
    params = {k: ",".join(sorted(v)) for k, v in sorted(params.items())}
    parameter = Section("Parameter", params)
    sections.append(parameter)

    sections.append(Section("Constraint"))

    return "\n\n".join(s.tostring() for s in sections)


def write(root: Node, filename: str):
    name, _ = splitext(filename)
    with open(filename, "w+") as f:
        f.write(toACTS(root, name))
