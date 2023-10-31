from Nodes.ConnectableGeneNode import *


class Contact(ConnectableGeneNode):
    def __init__(self, name, parent=None):
        super().__init__(name, parent, None)

    @property
    def X(self) -> int:
        """Положение контакта по оси X. Чем меньше тем левее"""
        return self.connector.leaves.index(self)
