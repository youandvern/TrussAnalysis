from PrattTrussGeometry.Geometry import Geometry


class Forces(object):
    """
    Class to generate force matrix for Pratt Truss geometry
    """
    def __init__(self, geometry):
        self.geometry = geometry
        self.forces = [0] * geometry.getNNodes()*2

    # positive direction is right and up
    def setForceAtNode(self, nodeIndex, forceX=0, forceY=0):
        self.forces[2 * nodeIndex] = forceX
        self.forces[2 * nodeIndex + 1] = forceY

    def setForceAtNodes(self, nodeIndexList, forceX=0, forceY=0):
        for i in nodeIndexList:
            self.setForceAtNode(i, forceX, forceY)
