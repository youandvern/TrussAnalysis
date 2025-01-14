from TrussAnalysis.TrussUtilities.Forces import Forces
from TrussAnalysis.Geometries.SemiParallelChordRoofTruss import Geometry

import StructPy.cross_sections as xs
import StructPy.materials as ma
import StructPy.Truss as Truss
import numpy as np


# Broken HSS in StructPy
class MyHSS(xs.HSS):
    @property
    def A(self):
        return self.B * self.H - self.b * self.h

    @property
    def xpts(self):
        x = self.B / 2
        xi = self.b / 2
        return [[-x, -xi], [x, xi], [x, xi], [-x, -xi], [-x, -xi]]

    @property
    def ypts(self):
        y = self.H / 2
        yi = self.h / 2
        return [[y, yi], [y, yi], [-y, -yi], [-y, -yi], [y, yi]]


# Example usage to analyze a Pratt style roof truss
def main():
    truss = Geometry(80, 12, 7, 6, 3)
    forces = Forces(truss.getNNodes())
    forces.setForceAtNodes(truss.getTopNodesIndices(), forceY=1.62)

    xs1 = MyHSS(2, 1.834, 2, 1.834)
    # xs1 = xs.AISC('HSS4X2X1/8')
    A992 = ma.A992()
    trussAnalysis = Truss.Truss(cross=xs1, material=A992)

    print("NODES ~~~~~~~~~~~~~~~~~~~~~~~~~ \n")
    for i, node in enumerate(truss.getNodes()):
        print(f"{node.x}, {node.y}, {node.fixity}, {forces.forces[2*i]}, {forces.forces[2*i+1]}")
        trussAnalysis.addNode(node.x, node.y, fixity=node.fixity)

    print("MEMBERS ~~~~~~~~~~~~~~~~~~~~~~~~~ \n")
    for mem in truss.getMembers():
        print(f"{mem.start}, {mem.end}, {xs1.A}, {A992.E}")
        trussAnalysis.addMember(mem.start, mem.end)

    print("\n")

    print(f"nodes match? {trussAnalysis.nNodes == truss.getNNodes()}")
    print(f"members match? {trussAnalysis.nMembers == truss.getNMembers()}")

    # Broken in StructPy
    # print(xs1.plot())
    # print(f"B = {xs1.B}")
    # print(f"H = {round(xs1.H, 4)}")
    # print(f"t = {round((xs1.H - xs1.h) / 2, 4)}")
    # print(f"A = {round(xs1.A, 4)}")
    # print(f"rx = {round(xs1.rx, 4)}")
    # print(f"ry = {round(xs1.ry, 4)}")
    # print(f"Sx = {round(xs1.Sx, 4)}")
    # print(f"Sy = {round(xs1.Sy, 4)}")
    # print(f"Ix = {round(xs1.Ix, 4)}")
    # print(f"Iy = {round(xs1.Iy, 4)}")
    # print(f"E = {A992.E}")

    deformation = trussAnalysis.directStiffness(np.array(forces.forces))
    # print(deformation)

    trussAnalysis.plot()

    np.set_printoptions(precision=0, linewidth=500)

    print('Stiffness Matrix, K')
    print(trussAnalysis.K)

    print('Reduced Stiffness Matrix')
    print(trussAnalysis.reducedK)

    print('External Load Matrix, Q')
    print(forces.forces)

    xDeform = []
    yDeform = []

    for i in range(len(deformation)):
        if (i % 2) == 0:
            xDeform.append(deformation[i])
        else:
            yDeform.append(deformation[i])

    print(f'Maximum downward displacement = {round(min(yDeform) * 12, 3)} in. at node {yDeform.index(min(yDeform))}')

    # BROKEN in StructPy
    # trussAnalysis.plotDeformation(scale=25)

    trussAnalysis.printNodes()

    trussAnalysis.printMembers()

    print(trussAnalysis.members[8].k)
    # print(trussAnalysis.members[8].kglobal.tolist())
    # print(trussAnalysis.freeDoF)


if __name__ == "__main__":
    main()