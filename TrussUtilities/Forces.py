class Forces(object):
    """
    Class to generate force matrix for Pratt Truss geometry
    """
    def __init__(self, nNodes):
        self.forces = [0] * nNodes*2

    # resets current force matrix to all 0s
    def resetForces(self):
        self.forces = [0] * len(self.forces)

    # positive direction is right and up
    def setForceAtNode(self, nodeIndex, forceX=0, forceY=0):
        self.forces[2 * nodeIndex] = forceX
        self.forces[2 * nodeIndex + 1] = forceY

    # positive direction is right and up
    def setForceAtNodes(self, nodeIndexList, forceX=0, forceY=0):
        for i in nodeIndexList:
            self.setForceAtNode(i, forceX, forceY)
