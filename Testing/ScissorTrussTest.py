from pytest import approx

import StructPy.cross_sections as xs
import StructPy.materials as ma
import StructPy.Truss as Truss
import numpy as np

from TrussAnalysis.TrussUtilities.Forces import Forces
from TrussAnalysis.Geometries.ScissorTruss import Geometry


def make_even_structure():
    truss = Geometry(16, 3, 6, 1)
    return truss


def make_odd_structure():
    truss = Geometry(16, 3, 3, 1)
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
    truss = make_odd_structure()
    forces = Forces(truss.getNNodes())
    forces.setForceAtNodes(truss.getTopNodesIndices(), forceY=-10)
    return forces.forces


def test_nodes_and_members():
    truss = make_odd_structure()
    assert truss.getNNodes() == len(truss.getNodes())
    assert truss.getNMembers() == len(truss.getMembers())

    truss = make_even_structure()
    assert truss.getNNodes() == len(truss.getNodes())
    assert truss.getNMembers() == len(truss.getMembers())


def test_odd_struct():
    truss = make_odd_structure()
    assert truss.getNNodes() == 10
    assert truss.getNMembers() == 17
    assert truss.getNodes()[4].y == 2
    assert truss.getNodes()[5].y == 3
    assert truss.getNodes()[7].y == 1


def test_even_struct():
    truss = make_even_structure()
    assert truss.getNNodes() == 16
    assert truss.getNMembers() == 29
    assert truss.getNodes()[7].y == 2
    assert truss.getNodes()[8].y == 3
    assert approx(truss.getNodes()[11].y, 0.001) == 1.7142857


def test_analysis_structure():
    truss = make_odd_structure()
    xs1, trussAnalysis = make_analysis_structure(truss)
    # trussAnalysis.plot()
    assert trussAnalysis.members[4].cross.A == xs1.A
    assert len(trussAnalysis.members) == truss.getNMembers()
    assert len(trussAnalysis.nodes) == truss.getNNodes()


def test_forces():
    forces = make_forces()
    assert forces[2] == 0  # node 1 x-dir
    assert forces[3] == -10  # node 1 y-dir
    assert forces[12] == 0  # node 7 x-dir
    assert forces[13] == -10  # node 7 y-dir
    assert forces[8] == 0
    assert forces[9] == 0


# Testing external library
def test_analysis():
    truss = make_odd_structure()
    xs1, trussAnalysis = make_analysis_structure(truss)
    forces = make_forces()
    trussAnalysis.directStiffness(np.array(forces))
    assert approx(trussAnalysis.members[0].axial, 0.001) == 213.6
    assert approx(trussAnalysis.members[4].axial, 0.001) == 170.880075
    assert approx(trussAnalysis.members[7].axial, 0.001) == -151.18054
    assert approx(trussAnalysis.members[11].axial, 0.001) == -15.7233


def test_top_nodes():
    truss = Geometry(16, 2, 1)
    assert truss.getTopNodesIndices() == [0, 1, 3, 4, 5]

    truss = Geometry(16, 2, 2)
    assert truss.getTopNodesIndices() == [0, 2, 4, 5, 7]

    truss = Geometry(16, 2, 3)
    assert truss.getTopNodesIndices() == [0, 1, 3, 5, 6, 8, 9]

    truss = Geometry(16, 2, 4)
    assert truss.getTopNodesIndices() == [0, 2, 4, 6, 7, 9, 11]

    truss = Geometry(16, 2, 6)
    assert truss.getTopNodesIndices() == [0, 2, 4, 6, 8, 9, 11, 13, 15]

    truss = Geometry(16, 2, 7)
    assert truss.getTopNodesIndices() == [0, 1, 3, 5, 7, 9, 10, 12, 14, 16, 17]


def test_bot_nodes():
    truss = Geometry(16, 2, 1)
    assert truss.getBotNodesIndices() == [0, 2, 5]

    truss = Geometry(16, 2, 2)
    assert truss.getBotNodesIndices() == [0, 1, 3, 6, 7]

    truss = Geometry(16, 2, 3)
    assert truss.getBotNodesIndices() == [0, 2, 4, 7, 9]

    truss = Geometry(16, 2, 4)
    assert truss.getBotNodesIndices() == [0, 1, 3, 5, 8, 10, 11]

    truss = Geometry(16, 2, 6)
    assert truss.getBotNodesIndices() == [0, 1, 3, 5, 7, 10, 12, 14, 15]

    truss = Geometry(16, 2, 7)
    assert truss.getBotNodesIndices() == [0, 2, 4, 6, 8, 11, 13, 15, 17]
