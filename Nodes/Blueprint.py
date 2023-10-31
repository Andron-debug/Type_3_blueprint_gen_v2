from Nodes.GeneNode import *
from Nodes.GroupOfContact import GroupOfContact
from Nodes.Connector import Connector
from Nodes.Contact import Contact

from deap import base

import matplotlib.pyplot as plt
from anytree import PostOrderIter
import copy


class Blueprint(GeneNode):
    def __init__(self, name, children: Iterable['GeneNode'] = None):
        super().__init__(name, None, children)
        self.fitness = FitnessMin()

    def add_empty_contacts(self):
        """Добавление пустых контактов в для уравнивания длин соединителей"""
        max_contact_count = max([len(node.leaves) for node in self.children])
        for connector in self.children:
            connector_children = list(connector.children)
            for i in range(len(connector.leaves), max_contact_count):
                connector_children.append(Contact(""))
            connector.children = connector_children

    @property
    def plot(self):
        for connector in self.children:
            contacts = connector.leaves
            plt.plot([-1, len(contacts) - 0.5], [connector.Y] * 2, "k--", linewidth=1)  # Вывод соединителей
            plt.text(-1, connector.Y, connector.name)  # Вывод подписи соединителей
            x = []
            y = []
            for contact in contacts:
                if contact.name != "":
                    x.append(contact.X)
                    y.append(contact.Y)
                else:
                    continue
                plt.text(x[-1] + 0.1, y[-1] + 0.02, contact.name, weight='bold')  # Вывод номеров контактов
                if len(contact.connection) != 0:
                    for connected_contact in contact.connection:
                        x_con = [connected_contact.X, x[-1]]
                        y_con = [connected_contact.Y, y[-1]]
                        plt.plot(x_con, y_con, 'k-', linewidth=1)  # Вывод жил между контактами проводов
            plt.scatter(x, y, color="black")  # Вывод контактов

            empty_x = [i for i, contact in enumerate(contacts) if contact.name == ""]  # Поиск пустых контактов
            plt.scatter(empty_x, [connector.Y] * len(empty_x), marker="x", color="red")  # Вывод пустых контактов

            group = [node for node in PostOrderIter(connector, filter_=lambda n: isinstance(n, GroupOfContact))]
            for i in range(len(group)):
                annotate_x = (group[i].leftX + group[i].rightX) / 2
                annotate_y = group[i].Y + ((i + 1) * 0.05) + rnd.uniform(0, 0.1)
                for contact in group[i].leaves:
                    plt.annotate("", xy=(contact.X, contact.Y), xytext=(annotate_x, annotate_y),
                                 arrowprops=dict(arrowstyle="->",
                                                 color="#FFC06F"))  # Вывод стрелок, указывающих на контакты группы
                # Вывод подписи к группе
                plt.text(annotate_x, annotate_y + 0.01, group[i].name, horizontalalignment='center', color="#FFC06F")

        plt.axis('off')
        return plt

    @staticmethod
    def mutate_blueprint(individual):
        """Мутация индивида"""
        to_mutate = rnd.sample([node for node in individual
                                if isinstance(node, (GroupOfContact, Connector))], ceil(individual.size / 10))
        for node in to_mutate:
            node.mutate()
        return individual,

    @staticmethod
    def mate_blueprint(individual1, individual2):
        """Скрещивание индивидов"""
        for node1, node2 in zip(individual1, individual2):
            if node1 == node2:
                node1.children, node2.children = Blueprint.__crossover_list(list(node1.children), list(node2.children))
        return individual1, individual2

    @staticmethod
    def __crossover_list(list1, list2):
        """
        Функция скрещивания списка. Равные элементы списка остаются неизменными. Позиции остальных меняются случайным
        образом
        :param list1:
            Список 1
        :param list2:
            Список 2
        :return:
            Два списка полученных в результате скрещивания
        """
        if len(list1) != len(list2):
            raise ValueError("Особи должны быть одной длинны")
        not_equal_index = []
        not_equal_list1 = []
        not_equal_list2 = []
        # Определение различных элементов и их индексов
        for i in range(len(list1)):
            if list1[i] != list2[i]:
                not_equal_index.append(i)
                not_equal_list1.append(list1[i])
                not_equal_list2.append(list2[i])
        # Размещение различающихся соединителей в случайном порядке
        rnd.shuffle(not_equal_list1)
        rnd.shuffle(not_equal_list2)
        j = 0
        for i in range(len(list1)):
            if i in not_equal_index:
                list1[i] = not_equal_list1[j]
                list2[i] = not_equal_list2[j]
                j += 1
        return list1, list2

    @staticmethod
    def create_individual(node):
        """Создание индивида"""
        node = copy.deepcopy(node)
        GeneNode.shuffle_tree(node)
        return node

    @staticmethod
    def evaluate(individual):
        """
        Оценка индивида.
        В для оценки схемы вычисляется расстояние (dist) между всеми подключенными ее компонентами.
        Расстоянием между двумя контактами считается манхеттенское расстояние между ними.
        Расстоянием между неделимой группой контактов и одиночным контактом считается манхеттенское расстояние между ним
        и крайним правым контактом группы.
        Расстоянием между двумя неделимыми группами контактов считается минимальное расстояние между двумя крайними
        контактами групп.
        """
        dist = 0  # Сумма расстояний
        fine = 0  # Штрафы
        bonus = 0  # Бонусы
        for node in individual:
            if isinstance(node, (Contact, GroupOfContact)):
                for connected_node in node.connection:
                    add_dist = 0
                    # Расстояние между двумя контактами
                    if isinstance(node, Contact) and isinstance(connected_node, Contact):
                        add_dist = abs(node.X - connected_node.X)
                        if add_dist == 0:  # Если прямые расположены на одной прямой
                            bonus += 1

                    # Расстояние неделимой группой контактов и одиночным контактом
                    if isinstance(node, Contact) and isinstance(connected_node, GroupOfContact):
                        add_dist = abs(node.X - connected_node.rightX)
                        if add_dist <= 1:
                            # Расстояние до подключенного контакта к экрану, меньше числа подключенных к нему контактов
                            bonus += 2



                    if isinstance(node, GroupOfContact) and isinstance(connected_node, Contact):
                        add_dist = abs(node.rightX - connected_node.X)
                        if add_dist <= 1:
                            # Расстояние до подключенного контакта к экрану, меньше числа подключенных к нему контактов
                            bonus += 2

                    # Расстояние между двумя группами контактов
                    if isinstance(node, GroupOfContact) and isinstance(connected_node, GroupOfContact):
                        add_dist = min(abs(node.rightX - connected_node.leftX), abs(node.leftX - connected_node.rightX))
                        if add_dist == 1:
                            # Если два подключенных экрана расположены рядом
                            bonus += 1

                    dist += add_dist
                    dist += abs(node.Y - connected_node.Y)
            """
            TODO
            Ввести штраф за линиями связей контактов
            """
        return 2*dist + fine - bonus,


class FitnessMin(base.Fitness):
    def __init__(self):
        """
        Присвоение весов для значений функции приспособленности. Это позволяет определить какие параметры
        для нас приоритетнее.
        """
        self.weights = -1,
