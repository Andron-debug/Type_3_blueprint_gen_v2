"""
Используемые библиотеки
Для генетического алгоритма deap 1.4.1
https://deap.readthedocs.io/en/master/api/tools.html
Работа с деревьями Any Python Tree Data
https://anytree.readthedocs.io/en/latest/index.html
"""
from Examples.E1 import settings, bp

from Nodes.GeneNode import GeneNode
from Nodes.Blueprint import Blueprint

from deap import base
from deap import tools
from deap import algorithms

import numpy
import matplotlib.pyplot as plt

bp.add_empty_contacts()
print(GeneNode.render_tree(bp))

# Метод register позволяет зарегистрировать в toolbox собственную функция
# toolbox.register(<Псевдоним>, <Функция>, <Параметр1>...<ПараметрN>)
toolbox = base.Toolbox()
toolbox.register("individual", Blueprint.create_individual, bp)

# Регистрация функции для создания индивидуума

# Регистрация функции вывода схемы
# toolbox.register("plot", create_plot, wires=wires)

# Регистрация функции для создания популяции
toolbox.register("population", tools.initRepeat, list, toolbox.individual)
pop = toolbox.population(settings["gen_size"])
pop.sort(key= Blueprint.evaluate)
pop[-1].plot.show()
# Регистрация функции для скрещивания
toolbox.register("mate", Blueprint.mate_blueprint)

# Регистрация функции для мутации
toolbox.register("mutate", Blueprint.mutate_blueprint)

# Регистрация функции отбора
toolbox.register("select", tools.selTournament, tournsize=10)

# Регистрация функции оценки
toolbox.register("evaluate", Blueprint.evaluate)

# Создание популяции
pop = toolbox.population(settings["gen_size"])

stats = tools.Statistics(lambda ind: ind.fitness.wvalues[0])
stats.register("best", numpy.max)

pop, log = algorithms.eaSimple(pop, toolbox,
                               cxpb=settings["cxpb"],
                               mutpb=settings["mutpb"],
                               ngen=settings["ngen"],
                               stats=stats)
pop.sort(key=Blueprint.evaluate)
pop[0].plot.show()
gen = log.select("gen")
fit_min = log.select("best")
plt.plot(gen, fit_min)
plt.xlabel("Поколение")
plt.ylabel("Лучшей результат")
plt.show()
