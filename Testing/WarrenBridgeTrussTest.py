from pytest import approx

import StructPy.cross_sections as xs
import StructPy.materials as ma
import StructPy.Truss as Truss
import numpy as np

from TrussAnalysis.TrussUtilities.Forces import Forces
from TrussAnalysis.Geometries.WarrenBridgeTruss import Geometry


def make_structure():
    truss = Geometry(16, 2, 3)
    return truss


def make_analysis_structure(truss):
    xs1 = xs.generalSection(1, 1, 1)
    randomMaterial = ma.Custom(1000, 10)
    trussAnalysis = Truss.Truss(cross=xs1, material=randomMaterial)

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
    assert truss.getNNodes() == 9
    assert truss.getNMembers() == 15
    assert truss.getTopNodesIndices() == [0, 1, 3, 5, 7, 8]
    assert truss.getNodes()[3].y == 4


def test_analysis_structure():
    truss = make_structure()
    xs1, trussAnalysis = make_analysis_structure(truss)
    # trussAnalysis.plot()
    assert trussAnalysis.members[4].cross.A == xs1.A
    assert len(trussAnalysis.members) == truss.getNMembers()
    assert len(trussAnalysis.nodes) == truss.getNNodes()


def test_forces():
    forces = make_forces()
    assert forces[0] == 0
    assert forces[1] == -10
    assert forces[14] == 0
    assert forces[15] == -10
    assert forces[8] == 0
    assert forces[9] == 0


# Testing external library
def test_analysis():
    truss = make_structure()
    xs1, trussAnalysis = make_analysis_structure(truss)
    forces = make_forces()
    trussAnalysis.directStiffness(np.array(forces))
    assert approx(trussAnalysis.members[0].axial, 0.001) == 25
    assert approx(trussAnalysis.members[5].axial, 0.001) == -15
    assert approx(trussAnalysis.members[9].axial, 0.001) == -12.5
    assert approx(trussAnalysis.members[14].axial, 0.001) == -12.5
