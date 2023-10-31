from Nodes.ConnectableGeneNode import ConnectableGeneNode
import random as rnd
from Nodes.Contact import Contact


class GroupOfContact(ConnectableGeneNode):
    def __init__(self, name, parent=None, children=None):
        super().__init__(name, parent, children)

    def add_empty_contact(self):
        """Вставка пустого контакта в случайное место группы"""
        list_of_children = list(self.children)
        list_of_children.insert(rnd.randint(0, len(list_of_children) - 1), Contact("", self))
        self.children = list_of_children

    @property
    def rightX(self) -> int:
        """Максимальная X координата контакта группы. Не учитываются пустые контакты c краю"""
        return max([cont.X for cont in self.leaves])

    @property
    def leftX(self) -> int:
        """Минимальная X координата контакта группы. Не учитываются пустые контакты c краю"""
        return min([cont.X for cont in self.leaves])
