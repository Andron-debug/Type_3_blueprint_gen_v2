from Nodes.GeneNode import *
from Nodes.Contact import Contact
class Connector(GeneNode):
    def __init__(self, name, parent=None, children=None):
        super().__init__(name, parent, children)

    def add_empty_contact(self):
        """Вставка пустого контакта в случайное место группы"""
        list_of_children = list(self.children)
        list_of_children.insert(rnd.randint(0, len(list_of_children) - 1), Contact("", self))
        self.children = list_of_children

    @property
    def Y(self):
        """Положение соединителя на схеме. Чем меньше индекс, тем ниже"""
        return self.root.children.index(self)
