from pytest import approx

import StructPy.cross_sections as xs
import StructPy.materials as ma
import StructPy.Truss as Truss
import numpy as np

from TrussAnalysis.TrussUtilities.Forces import Forces
from TrussAnalysis.Geometries.PrattRoofTruss import Geometry


# Fixed Area Calc
class MyHSS(xs.HSS):
    @property
    def A(self):
        return self.B * self.H - self.b * self.h


def make_structure():
    truss = Geometry(28, 4.083, 1)
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
    forces.setForceAtNodes(truss.getTopNodesIndices(), forceY=-1.24)
    forces.setForceAtNode(0, forceY=-0.620)
    forces.setForceAtNode(truss.getNNodes()-1, forceY=-0.620)
    return forces.forces


def test_struct():
    truss = make_structure()
    assert truss.getNNodes() == 8
    assert truss.getNMembers() == 13
    assert truss.getTopNodesIndices() == [0, 1, 3, 5, 7]
    assert truss.getNodes()[3].y == 4.083


def test_analysis_structure():
    truss = make_structure()
    xs1, trussAnalysis = make_analysis_structure(truss)
    assert trussAnalysis.members[4].cross.A == xs1.A
    assert len(trussAnalysis.members) == truss.getNMembers()
    assert len(trussAnalysis.nodes) == truss.getNNodes()


def test_forces():
    forces = make_forces()
    assert forces[0] == 0
    assert forces[1] == -0.620
    assert forces[6] == 0
    assert forces[7] == -1.24
    assert forces[12] == 0
    assert forces[13] == 0


# Testing external library
def test_analysis():
    truss = make_structure()
    xs1, trussAnalysis = make_analysis_structure(truss)
    forces = make_forces()
    trussAnalysis.directStiffness(np.array(forces))
    assert approx(trussAnalysis.members[0].axial, 0.001) == 6.64
    assert approx(trussAnalysis.members[2].axial, 0.001) == 4.43
    assert approx(trussAnalysis.members[4].axial, 0.001) == -6.38
    assert approx(trussAnalysis.members[12].axial, 0.001) == 0.0


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
    assert approx(trussAnalysis.members[0].axial, 0.01) == 15.146
    assert approx(trussAnalysis.members[0].length, 0.01) == 8.975

    assert approx(trussAnalysis.members[3].axial, 0.01) == 9.087
    assert approx(trussAnalysis.members[7].axial, 0.01) == -14.0625
    assert approx(trussAnalysis.members[18].axial, 0.01) == -1.125


def test_alt_design_nodes_moved():
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

    print(list(map(lambda n: (n.x, n.y), nodes)))

    for node in nodes:
        trussAnalysis.addNode(node.x, node.y, fixity=node.fixity)

    for mem in truss.getMembers():
        trussAnalysis.addMember(mem.start, mem.end)

    forces = Forces(truss.getNNodes())
    forces.setForceAtNodes(truss.getTopNodesIndices(), forceY=-2.25)
    forces.setForceAtNode(0, forceY=-1.12)
    forces.setForceAtNode(truss.getNNodes() - 1, forceY=-1.12)

    trussAnalysis.directStiffness(np.array(forces.forces))
    trussAnalysis.plot()
    assert approx(trussAnalysis.members[0].axial, 0.01) == 15.146
    assert approx(trussAnalysis.members[0].length, 0.01) == 8.975

    assert approx(trussAnalysis.members[3].axial, 0.01) == 9.087
    assert approx(trussAnalysis.members[7].axial, 0.01) == -14.0625
    assert approx(trussAnalysis.members[18].axial, 0.01) == -1.125
