from dataclasses import dataclass, field
from typing import Optional

from pydrawio.mxgraphmodel import MxCell


@dataclass
class Node:
    id: str
    value: str
    style: dict[str, object]
    parent: Optional['Node'] = None
    children: list['Node'] = field(default_factory=list)

    def __repr__(self):
        return f"<{self.value}>" if self.is_class() else f"'{self.value}'"

    @classmethod
    def from_xml(cls, xml: MxCell):
        style = {}
        for entry in xml.style.strip().split(";"):
            key, *value = entry.strip().split("=", maxsplit=1)
            if value:
                style[key] = value[0]
            else:
                style[key] = True
        return cls(xml.id, xml.value, style)

    def is_root(self):
        return not self.parent and self.children

    def is_class(self):
        # return self.style.get("strokeColor", False) == "none"
        return not self.children

    def dfs(self):
        yield self
        for node in self.children:
            yield from node.dfs()

    def prettify(self, depth=0) -> str:
        res = "--" * depth + " " * bool(depth) + str(self)
        for node in self.children:
            res += "\n" + node.prettify(depth + 1)
        return res
