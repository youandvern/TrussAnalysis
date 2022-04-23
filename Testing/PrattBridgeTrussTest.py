from pytest import approx

import StructPy.cross_sections as xs
import StructPy.materials as ma
import StructPy.Truss as Truss
import numpy as np

from TrussAnalysis.TrussUtilities.Forces import Forces
from TrussAnalysis.Geometries.PrattBridgeTruss import Geometry


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
    assert truss.getNodes()[3].y == 4


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
    assert forces[14] == 0
    assert forces[15] == -10
    assert forces[20] == 0
    assert forces[21] == 0


# Testing external library
def test_analysis():
    truss = make_structure()
    xs1, trussAnalysis = make_analysis_structure(truss)
    forces = make_forces()
    trussAnalysis.directStiffness(np.array(forces))
    assert approx(trussAnalysis.members[0].axial, 0.001) == 35.355
    assert approx(trussAnalysis.members[6].axial, 0.001) == -25
    assert approx(trussAnalysis.members[16].axial, 0.001) == 10
    assert approx(trussAnalysis.members[20].axial, 0.001) == 0.0
