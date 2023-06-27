from TrussAnalysis.TrussUtilities.MemberType import MemberType
from TrussAnalysis.TrussUtilities.Node import Node
from TrussAnalysis.TrussUtilities.Member import Member


class Geometry(object):
    """
    Class to generate nodes and members for Warren Bridge Truss geometry
    """
    def __init__(self, span, height, nVertWebsPerSide=1, trussDepth=None):
        self.span = span
        self.height = height
        self.trussDepth = height if trussDepth is None else trussDepth
        self.nWeb = nVertWebsPerSide

    def getNNodes(self):
        return 2 * self.nWeb + 3

    def getNMembers(self):
        return 4 * self.nWeb + 3

    def getPitch(self):
        return 0

    def getNodes(self):
        nNodes = self.getNNodes()
        horSpacing = self.span / (nNodes - 1)
        nodes = []
        botNode = True

        for i in range(0, nNodes):
            nodes.append(Node(i * horSpacing, 0 if botNode else self.height))
            botNode = not botNode

        nodes[0].fixity = 'pin'  # left support
        nodes[-1].fixity = 'roller'  # right support
        return nodes

    def getMembers(self):
        nNodes = self.getNNodes()
        members = []

        for i in range(1, nNodes + 1, 2):
            members.append(Member(max(0, i - 2), min(i, nNodes - 1), MemberType.topChord))

        for i in range(0, nNodes - 1, 2):
            members.append(Member(i, i + 2, MemberType.botChord))

        for i in range(1, nNodes - 2):
            members.append((Member(i, i + 1, MemberType.diaWeb)))

        return members

    # left to right
    def getTopNodesIndices(self):
        nNodes = self.getNNodes()
        topNodeIndices = []
        topNodeIndices.append(0)
        for i in range(1, nNodes - 1, 2):
            topNodeIndices.append(i)
        topNodeIndices.append(nNodes - 1)
        return topNodeIndices

    # left to right
    def getBotNodesIndices(self):
        nNodes = self.getNNodes()
        botNodeIndices = []
        for i in range(0, nNodes, 2):
            botNodeIndices.append(i)
        return botNodeIndices

    # left to right
    def getTopWebNodesIndices(self):
        return self.getTopNodesIndices()[1: -1]

    # left to right
    def getBotWebNodesIndices(self):
        return self.getBotNodesIndices()[1: -1]
