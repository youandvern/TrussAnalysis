from TrussAnalysis.TrussUtilities.MemberType import MemberType
from TrussAnalysis.TrussUtilities.Node import Node
from TrussAnalysis.TrussUtilities.Member import Member


class Geometry(object):
    """
    Class to generate nodes and members for Fink Roof Truss geometry
    """
    def __init__(self, span, height, nVertWebsPerSide=1):
        self.span = span
        self.height = height
        self.nWeb = nVertWebsPerSide

    def getNNodes(self):
        return 4 * self.nWeb + 3

    def getNMembers(self):
        return 8 * self.nWeb + 3

    def getPitch(self):
        return self.height / self.span

    def getNodes(self):
        nNodes = self.getNNodes()
        horSpacingTop = self.span / (2*self.nWeb+2)
        horSpacingBot = self.span / (2*self.nWeb+1)
        nodes = []
        nodes.append(Node(0, 0, fixity='pin'))  # left support

        for i in range(1, (nNodes // 2) + 1):
            xit = horSpacingTop * i
            xib = horSpacingBot * i
            hit = min(xit * 2 * self.height / self.span, 2 * self.height - xit * 2 * self.height / self.span)
            nodes.append(Node(xit, hit))  # upper
            nodes.append(Node(xib, 0))  # lower

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
        topWebNodeIndices = self.getTopNodesIndices()
        removeNodes = [topWebNodeIndices[0],
                       topWebNodeIndices[len(topWebNodeIndices) // 2],
                       topWebNodeIndices[- 1]]

        for i in removeNodes:
            topWebNodeIndices.remove(i)

        return topWebNodeIndices

    # left to right
    def getBotWebNodesIndices(self):
        botWebNodeIndices = self.getBotNodesIndices()
        removeNodes = [botWebNodeIndices[0],
                       botWebNodeIndices[- 1]]

        for i in removeNodes:
            botWebNodeIndices.remove(i)

        return botWebNodeIndices

