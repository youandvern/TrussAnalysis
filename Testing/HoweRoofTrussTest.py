from pytest import approx

import StructPy.cross_sections as xs
import StructPy.materials as ma
import StructPy.Truss as Truss
import numpy as np

from TrussAnalysis.TrussUtilities.Forces import Forces
from TrussAnalysis.Geometries.HoweRoofTruss import Geometry


# Fixed Area Calc
class MyHSS(xs.HSS):
    @property
    def A(self):
        return self.B * self.H - self.b * self.h


def make_structure():
    truss = Geometry(24, 4, 2)
    return truss


def make_analysis_structure(truss):
    xs1 = MyHSS(2, 1.834, 2, 1.834)
    # xs1 = xs.AISC('HSS4X2X1/8')
    A992 = ma.A992()
    trussAnalysis = Truss.Truss(cross=xs1, material=A992)

    for node in truss.getNodes():
        trussAnalysis.addNode(node.x, node.y, fixity=node.fixity)

    for mem in truss.getMembers():
        trussAnalysis.addMember(mem.start, mem.end)

    return xs1, trussAnalysis


def make_forces():
    truss = make_structure()
    forces = Forces(truss.getNNodes())
    forces.setForceAtNodes(truss.getTopNodesIndices(), forceY=-10)
    return forces.forces


def test_struct():
    truss = make_structure()
    assert truss.getNNodes() == 12
    assert truss.getNMembers() == 21
    assert truss.getTopNodesIndices() == [0, 1, 3, 5, 7, 9, 11]
    assert truss.getNodes()[5].y == 4


def test_analysis_structure():
    truss = make_structure()
    xs1, trussAnalysis = make_analysis_structure(truss)
    assert trussAnalysis.members[4].cross.A == xs1.A
    assert len(trussAnalysis.members) == truss.getNMembers()
    assert len(trussAnalysis.nodes) == truss.getNNodes()


def test_forces():
    forces = make_forces()
    assert forces[0] == 0
    assert forces[1] == -10
    assert forces[6] == 0
    assert forces[7] == -10
    assert forces[12] == 0
    assert forces[13] == 0


# Testing external library
def test_analysis():
    truss = make_structure()
    xs1, trussAnalysis = make_analysis_structure(truss)
    forces = make_forces()
    trussAnalysis.directStiffness(np.array(forces))
    assert approx(trussAnalysis.members[0].axial, 0.001) == 79.06
    assert approx(trussAnalysis.members[6].axial, 0.001) == -75
    assert approx(trussAnalysis.members[12].axial, 0.001) == 10


def test_original_design():
    truss = Geometry(50, 10, 2)

    print(list(map(lambda n: (n.x, n.y), truss.getNodes())))

    xs1 = MyHSS(4, 4-2*0.116, 2, 2-2*0.116)
    # xs1 = xs.AISC('HSS4X2X1/8')
    A992 = ma.A992()
    trussAnalysis = Truss.Truss(cross=xs1, material=A992)

    for node in truss.getNodes():
        trussAnalysis.addNode(node.x, node.y, fixity=node.fixity)

    for mem in truss.getMembers():
        trussAnalysis.addMember(mem.start, mem.end)

    forces = Forces(truss.getNNodes())
    forces.setForceAtNodes(truss.getTopNodesIndices(), forceY=-2.25)
    forces.setForceAtNode(0, forceY=-1.12)
    forces.setForceAtNode(truss.getNNodes() - 1, forceY=-1.12)

    trussAnalysis.directStiffness(np.array(forces.forces))
    assert approx(trussAnalysis.members[0].axial, 0.01) == 15.147
    assert approx(trussAnalysis.members[0].length, 0.01) == 8.975

    assert approx(trussAnalysis.members[3].axial, 0.01) == 12.117
    assert approx(trussAnalysis.members[7].axial, 0.01) == -11.25
    assert approx(trussAnalysis.members[18].axial, 0.01) == 3.375


def test_alt_design_nodes_shifted():
    truss = Geometry(50, 10, 2)

    xs1 = MyHSS(4, 4-2*0.116, 2, 2-2*0.116)
    # xs1 = xs.AISC('HSS4X2X1/8')
    A992 = ma.A992()
    trussAnalysis = Truss.Truss(cross=xs1, material=A992)

    nodes = truss.getNodes()
    nodes[2].x = 11.3125
    nodes[2].fixity = "roller"
    nodes[8].x = 34.5625
    nodes[8].fixity = "roller"

    nodes[4].x = 18.5

    print(list(map(lambda n: (n.x, n.y), nodes)))

    for node in nodes:
        print(f'[{node.x}, {node.y}, "{node.fixity}"],')
        trussAnalysis.addNode(node.x, node.y, fixity=node.fixity)

    for mem in truss.getMembers():
        print(f'[{mem.start}, {mem.end}],')
        trussAnalysis.addMember(mem.start, mem.end)

    forces = Forces(truss.getNNodes())
    forces.setForceAtNodes(truss.getTopNodesIndices(), forceY=-2.25)
    forces.setForceAtNode(0, forceY=-1.12)
    forces.setForceAtNode(truss.getNNodes() - 1, forceY=-1.12)

    trussAnalysis.directStiffness(np.array(forces.forces))
    trussAnalysis.plot()
    for i in range(len(trussAnalysis.members)):
        print(f'Mem #{i}    len = {trussAnalysis.members[i].length}         f = {trussAnalysis.members[i].axial}')


def test_alt_1_design_nodes_removed():

    nodes = [
        [0.0, 0.0, "pin"],
        [8.333333333333334, 3.333333333333334, "free"],
        [11.3125, 0.0, "roller"],
        [16.666666666666668, 6.666666666666668, "free"],
        [25.0, 10.0, "free"],
        [25.0, 0.0, "free"],
        [33.333333333333336, 6.666666666666664, "free"],
        [34.5625, 0.0, "roller"],
        [41.66666666666667, 3.3333333333333286, "free"],
        [50, 0.0, "roller"]
    ]

    top_nodes = []
    for i in range(len(nodes)):
        if nodes[i][1] != 0.0:
            top_nodes.append(i)

    members = [
        [0, 1],
        [1, 3],
        [3, 4],
        [4, 6],
        [6, 8],
        [8, 9],
        [0, 2],
        [2, 5],
        [5, 7],
        [7, 9],
        [1, 2],
        [2, 3],
        [3, 5],
        [4, 5],
        [5, 6],
        [6, 7],
        [7, 8]
    ]




    xh = 2 / 12
    xh_inner = (2 - 2 * 0.083) / 12
    xs1 = MyHSS(xh, xh_inner, xh, xh_inner)
    # print(f'Ag = {xs1.A}  --  rx = {xs1.rx}')
    # xs1 = xs.AISC('HSS4X2X1/8')
    steel = ma.Custom(E=41760000)
    trussAnalysis = Truss.Truss(cross=xs1, material=steel)

    for node in nodes:
        trussAnalysis.addNode(node[0], node[1], fixity=node[2])

    for mem in members:
        trussAnalysis.addMember(mem[0], mem[1])

    forces = Forces(len(nodes))
    forces.setForceAtNodes(top_nodes, forceY=-2.25)
    forces.setForceAtNode(0, forceY=-1.12)
    forces.setForceAtNode(len(nodes) - 1, forceY=-1.12)

    print("p")
    print("~~~~~~~~NODES")
    for i in range(0, len(forces.forces), 2):
        node = nodes[i//2]
        print(f'{node[0]}, {node[1]}, {node[2]}, {forces.forces[i]}, {-1 * forces.forces[i+1]}')

    deflections = trussAnalysis.directStiffness(np.array(forces.forces))
    print("deflections")
    for i in range(0, len(deflections), 2):
        print(f'Node {i}, {round(deflections[i], 5)}, {round(deflections[i+1], 5)}')

    # trussAnalysis.plot(labels=True)

    global_f = list(np.round(np.dot(trussAnalysis.K, deflections), decimals=3))

    print("forces")
    print("Node #   Fx (kips)   Fy (kips)")
    for i in range(0, len(global_f), 2):
        print(f'#{i//2}  x = {global_f[i]}   y = {global_f[i+1]}')

    print("~~~~~~MEMBERS")
    for mem in members:
        print(f'{mem[0]}, {mem[1]}, 0.62, 29000')
    for i in range(len(trussAnalysis.members)):
        # member = trussAnalysis.members[i]
        print(f'Mem {i}, {round(trussAnalysis.members[i].length, 2)}, {round(trussAnalysis.members[i].axial, 2)}')
        print(f'Mem #{i}    len = {trussAnalysis.members[i].length}         f = {trussAnalysis.members[i].axial}')
    assert approx(trussAnalysis.members[0].axial, 0.01) == 15.146
    assert approx(trussAnalysis.members[0].length, 0.01) == 8.975

    assert approx(trussAnalysis.members[3].axial, 0.01) == 9.087
    assert approx(trussAnalysis.members[7].axial, 0.01) == -14.0625
    assert approx(trussAnalysis.members[18].axial, 0.01) == -1.125


def test_al_2_design_nodes_removed():

    nodes = [
        [0.0, 0.0, "pin"],
        [8.333333333333334, 3.333333333333334, "free"],
        [11.3125, 0.0, "roller"],
        [16.666666666666668, 6.666666666666668, "free"],
        [25.0, 10.0, "free"],
        [25.0, 0.0, "free"],
        [33.333333333333336, 6.666666666666664, "free"],
        [38.6875, 0.0, "roller"],
        [41.66666666666667, 3.3333333333333286, "free"],
        [50, 0.0, "roller"]
    ]

    top_nodes = []
    for i in range(len(nodes)):
        if nodes[i][1] != 0.0:
            top_nodes.append(i)

    members = [
        [0, 1],
        [1, 3],
        [3, 4],
        [4, 6],
        [6, 8],
        [8, 9],
        [0, 2],
        [2, 5],
        [5, 7],
        [7, 9],
        [1, 2],
        [2, 3],
        [3, 5],
        [4, 5],
        [5, 6],
        [6, 7],
        [7, 8]
    ]

    xh = 2 / 12
    xh_inner = (2 - 2 * 0.083) / 12
    xs1 = MyHSS(xh, xh_inner, xh, xh_inner)
    # print(f'Ag = {xs1.A}  --  rx = {xs1.rx}')
    # xs1 = xs.AISC('HSS4X2X1/8')
    steel = ma.Custom(E=41760000)
    trussAnalysis = Truss.Truss(cross=xs1, material=steel)

    for node in nodes:
        trussAnalysis.addNode(node[0], node[1], fixity=node[2])

    for mem in members:
        trussAnalysis.addMember(mem[0], mem[1])

    forces = Forces(len(nodes))
    forces.setForceAtNodes(top_nodes, forceY=-2.25)
    forces.setForceAtNode(0, forceY=-1.12)
    forces.setForceAtNode(len(nodes) - 1, forceY=-1.12)

    print("p")
    print("~~~~~~~~NODES")
    for i in range(0, len(forces.forces), 2):
        node = nodes[i // 2]
        print(f'{node[0]}, {node[1]}, {node[2]}, {forces.forces[i]}, {-1 * forces.forces[i + 1]}')

    deflections = trussAnalysis.directStiffness(np.array(forces.forces))
    print("deflections")
    for i in range(0, len(deflections), 2):
        print(f'Node {i}, {round(deflections[i], 5)}, {round(deflections[i + 1], 5)}')

    trussAnalysis.plot(labels=True)

    global_f = list(np.round(np.dot(trussAnalysis.K,deflections), decimals=3))

    print("forces")
    print("Node #   Fx (kips)   Fy (kips)")
    for i in range(0, len(global_f), 2):
        print(f'#{i//2}  x = {global_f[i]}   y = {global_f[i+1]}')

    print("~~~~~~MEMBERS")
    for mem in members:
        print(f'{mem[0]}, {mem[1]}, 0.62, 29000')
    for i in range(len(trussAnalysis.members)):
        print(f'Mem {i}, {round(trussAnalysis.members[i].length, 4)}, {round(trussAnalysis.members[i].axial, 4)}')
        # print(f'Mem #{i}    len = {trussAnalysis.members[i].length}         f = {trussAnalysis.members[i].axial}')
    assert approx(trussAnalysis.members[0].axial, 0.01) == 15.146
    assert approx(trussAnalysis.members[0].length, 0.01) == 8.975

    assert approx(trussAnalysis.members[3].axial, 0.01) == 9.087
    assert approx(trussAnalysis.members[7].axial, 0.01) == -14.0625
    assert approx(trussAnalysis.members[18].axial, 0.01) == -1.125
