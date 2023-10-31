from Nodes.Blueprint import Blueprint
from Nodes.Connector import Connector
from Nodes.GroupOfContact import GroupOfContact
from Nodes.Contact import Contact

settings = {"cxpb": 0.5, "mutpb": 0.3, "ngen": 20, "gen_size": 500}

bp = Blueprint("Схема 1")

xp1 = Connector("XP1", bp)
xp1_contacts = [Contact(i) for i in range(12)]
xp1_sh1 = GroupOfContact("XP1_SH1", xp1)
xp1_tw1 = GroupOfContact("XP1_TW1", xp1_sh1, [xp1_contacts[0], xp1_contacts[1]])
xp1_tw2 = GroupOfContact("XP1_TW2", xp1_sh1, [xp1_contacts[2], xp1_contacts[3]])
xp1_contacts[4].parent = xp1
xp1_contacts[5].parent = xp1
xp1_contacts[6].parent = xp1
xp1_tw1.connection = [xp1_contacts[4], xp1_contacts[5], xp1_contacts[6]]
xp1_sh2 = GroupOfContact("XP1_SH3", xp1)
xp1_sh3 = GroupOfContact("XP1_SH4", xp1)
xp1_sh2.addConnection(xp1_sh3)
xp1_contacts[11].parent = xp1
xp1_sh3.addConnection(xp1_contacts[11])
xp1_sh2.children = [xp1_contacts[7], xp1_contacts[8]]
xp1_sh3.children = [xp1_contacts[9], xp1_contacts[10]]

xp2 = Connector("XP2", bp)
xp2_contacts = [Contact(i) for i in range(9)]
xp2_sh1 = GroupOfContact("XP2_SH2", xp2)
xp2_tw1 = GroupOfContact("XP2_TW2", xp2_sh1, [xp2_contacts[0], xp2_contacts[1]])
xp2_tw2 = GroupOfContact("XP2_TW2", xp2_sh1, [xp2_contacts[2], xp2_contacts[3]])
xp2_sh2 = GroupOfContact("XP2_SH3", xp2)
xp2_sh3 = GroupOfContact("XP2_SH4", xp2)
xp2_sh2.addConnection(xp2_sh3)
xp2_contacts[8].parent = xp2
xp2_sh3.addConnection(xp2_contacts[8])
xp2_sh2.children = [xp2_contacts[4], xp2_contacts[5]]
xp2_sh3.children = [xp2_contacts[6], xp2_contacts[7]]


for i in range(0, 4):
    xp1_contacts[i].addConnection(xp2_contacts[i])

xp1_contacts[7].addConnection(xp2_contacts[4])
xp1_contacts[8].addConnection(xp2_contacts[5])
xp1_contacts[9].addConnection(xp2_contacts[6])
xp1_contacts[10].addConnection(xp2_contacts[7])