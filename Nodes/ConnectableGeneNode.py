from Nodes.GeneNode import GeneNode
from typing import List
from abc import ABC


class ConnectableGeneNode(GeneNode, ABC):
    def __init__(self, name, parent=None, children=None):
        super().__init__(name, parent, children)
        self.connection: List[ConnectableGeneNode] = []

    @property
    def connector(self):
        """Сoeдинитель, в состав которого входит контакт (группа контактов)"""
        return self.ancestors[1]

    def addConnection(self, other: "ConnectableGeneNode"):
        self.connection.append(other)

    @property
    def Y(self) -> int:
        return self.connector.Y
