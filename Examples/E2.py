from Nodes.Blueprint import Blueprint
from Nodes.Connector import Connector
from Nodes.GroupOfContact import GroupOfContact
from Nodes.Contact import Contact

settings = {"cxpb": 0.5, "mutpb": 0.3, "ngen": 20, "gen_size": 500}
bp = Blueprint("Схема 1")
xp1 = Connector("XP1", bp)
xp1_con = [Contact(i) for i in range(8)]
xp1_sh1 = GroupOfContact("XP1_SH1", xp1, [xp1_con[0], xp1_con[1]])
xp1_con[2].parent = xp1
xp1_sh1.addConnection(xp1_con[2])
xp1_sh2 = GroupOfContact("XP1_SH2", xp1, [xp1_con[3], xp1_con[4]])
xp1_sh3 = GroupOfContact("XP1_SH3", xp1, [xp1_con[5], xp1_con[6]])
xp1_con[7].parent = xp1
xp1_sh2.addConnection(xp1_sh3)
xp1_sh3.addConnection(xp1_con[7])

xp2 = Connector("XP2", bp)
xp2_con = [Contact(i) for i in range(6)]
xp2_sh1 = GroupOfContact("XP2_SH1", xp2, [xp2_con[0], xp2_con[1]])
xp2_con[2].parent = xp2
xp2_sh1.addConnection(xp2_con[2])
xp2_sh3 = GroupOfContact("XP2_SH3", xp2, [xp2_con[3], xp2_con[4]])
xp2_con[5].parent = xp2
xp2_sh3.addConnection(xp2_con[5])

xp3 = Connector("XP3", bp)
xp3_con = [Contact(i) for i in range(3)]
xp3_sh1 = GroupOfContact("XP3_SH2", xp3, [xp3_con[0], xp3_con[1]])
xp3_con[2].parent = xp3
xp3_sh1.addConnection(xp3_con[2])

for i in range(2):
    xp1_con[i].addConnection(xp2_con[i])
for i in range(2):
    xp3_con[i].addConnection(xp1_con[i+3])
for i in range(2):
    xp2_con[i+3].addConnection(xp1_con[i+5])

