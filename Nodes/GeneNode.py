import random as rnd
from abc import ABC
from typing import Iterable
from anytree import NodeMixin, RenderTree, PreOrderIter
from math import ceil


class GeneNode(NodeMixin, ABC):
    def __init__(self, name, parent: 'GeneNode' = None, children: Iterable['GeneNode'] = None):
        self.parent: GeneNode = parent
        self.name: str = name
        if children:
            self.children: Iterable['GeneNode'] = children

    def shuffle(self):
        """Перемешивание позиций дочерних элементов"""
        children = list(self.children)
        rnd.shuffle(children)
        self.children = children

    def mutate(self):
        """Метод меняет местами расположение двух случайных дочерних элементов и"""
        children = list(self.children)
        if len(children) != 0:
            p1 = rnd.randint(0, len(children) - 1)
            p2 = rnd.randint(0, len(children) - 1)
            # while children[p1].name == children[p2].name:
            #     # Нельзя менять местами два пустых контакта
            #     p1 = rnd.randint(0, len(children) - 1)
            #     p2 = rnd.randint(0, len(children) - 1)
            children[p1], children[p2] = children[p2], children[p1]
            self.children = children

    def __eq__(self, other):
        return self.name == other.name and self.parent == other.parent

    def __str__(self):
        if self.parent is not None:
            return f"Имя:{self.name} Родитель:{self.parent.name} Тип:{self.__class__.__name__}"
        return f"Имя:{self.name} Тип: {self.__class__.__name__}"

    def __iter__(self):
        return PreOrderIter(self)

    @staticmethod
    def shuffle_tree(node):
        """Перемешивание позиций всех элементов дерева"""
        for node in PreOrderIter(node):
            node.shuffle()

    @staticmethod
    def render_tree(tree):
        result = ""
        for pre, _, node in RenderTree(tree):
            tree_str = u"%s %s %s" % (pre, "Имя:", node.name)
            result += f"{tree_str.ljust(8)} Тип: {node.__class__.__name__}\n"
        return result.strip()
