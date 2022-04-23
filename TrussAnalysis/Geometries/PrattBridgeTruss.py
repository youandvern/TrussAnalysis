from TrussAnalysis.TrussUtilities.MemberType import MemberType
from TrussAnalysis.TrussUtilities.Node import Node
from TrussAnalysis.TrussUtilities.Member import Member


class Geometry(object):
    """
    Class to generate nodes and members for Pratt Truss geometry
    """
    def __init__(self, span, height, nVertWebsPerSide=1):
        self.span = span
        self.height = height
        self.nWeb = nVertWebsPerSide

    def getNNodes(self):
        return 4 * self.nWeb + 4

    def getNMembers(self):
        return 8 * self.nWeb + 5

    def getPitch(self):
        return 0

    def getNodes(self):
        nNodes = self.getNNodes()
        horSpacing = self.span / (2*self.nWeb+2)
        nodes = []
        nodes.append(Node(0, 0, fixity='pin'))  # left support

        for i in range(1, (nNodes // 2)):
            xi = horSpacing * i
            nodes.append(Node(xi, self.height))  # upper
            nodes.append(Node(xi, 0))  # lower

        nodes.append(Node(self.span, 0, fixity='roller'))  # right support

        return nodes

    def getMembers(self):
        nNodes = self.getNNodes()
        members = []

        for i in range(1, nNodes, 2):
            members.append(Member(max(0, i - 2), i, MemberType.topChord))

        for i in range(0, nNodes, 2):
            members.append(Member(i, min(i + 2, nNodes - 1), MemberType.botChord))

        # Left web
        for i in range(1, self.nWeb * 2, 2):
            members.append(Member(i, i+1, MemberType.vertWeb))
            members.append(Member(i, i+3, MemberType.diaWeb))

        # Center post
        members.append(Member((nNodes // 2) - 1, nNodes // 2, MemberType.vertWeb))

        # Right web
        for i in range(nNodes // 2, nNodes - 2):
            memType = MemberType.diaWeb if i // 2 == 0 else MemberType.vertWeb
            members.append(Member(i, i + 1, memType))

        return members

    # left to right
    def getTopNodesIndices(self):
        nNodes = self.getNNodes()
        topNodeIndices = []
        topNodeIndices.append(0)
        for i in range(1, nNodes, 2):
            topNodeIndices.append(i)
        return topNodeIndices

    # left to right
    def getBotNodesIndices(self):
        nNodes = self.getNNodes()
        botNodeIndices = []
        for i in range(0, nNodes, 2):
            botNodeIndices.append(i)
        botNodeIndices.append(nNodes - 1)
        return botNodeIndices

    # left to right
    def getTopWebNodesIndices(self):
        return self.getTopNodesIndices()[1: -1]

    # left to right
    def getBotWebNodesIndices(self):
        return self.getBotNodesIndices()[1: -1]

