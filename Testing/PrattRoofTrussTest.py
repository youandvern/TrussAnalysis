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
