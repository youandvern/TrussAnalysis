from PrattTrussGeometry.MemberType import MemberType
from PrattTrussGeometry.Node import Node
from PrattTrussGeometry.Member import Member


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
        return self.height / self.span

    def getNodes(self):
        nNodes = self.getNNodes()
        horSpacing = self.span / (2*nNodes+2)
        nodes = []
        nodes.append(Node(0, 0, fixity='pin'))  # left support
        nodes.append(Node(self.span, 0, fixity='roller'))  # right support

        for i in range(1, self.nWeb + 1):
            xi = horSpacing * i
            hi = xi * 2 * self.height / self.span
            nodes.append(Node(xi, 0))  # lower left
            nodes.append(Node(self.span - xi, 0))  # lower right
            nodes.append(Node(xi, hi))  # upper left
            nodes.append(Node(self.span - xi, hi))  # upper right

        nodes.append(Node(self.span / 2, 0))  # center top
        nodes.append(Node(self.span / 2, self.height))  # center bot

        return nodes

    def getMembers(self):
        nNodes = self.getNNodes()
        members = []
        members.append(Member(0, 2, MemberType.botChord))  # bot left corner
        members.append(Member(1, 3, MemberType.botChord))  # bot right corner
        members.append(Member(0, 4, MemberType.topChord))  # top left corner
        members.append(Member(1, 5, MemberType.topChord))  # top right corner
        members.append(Member(nNodes - 1, nNodes, MemberType.vertWeb))  # center web
        for i in range(1, self.nWeb + 1):
            # left side
            members.append(Member(4 * i - 2, 4 * i, MemberType.vertWeb))
            members.append(Member(4 * i - 2, 4 * i + 2, MemberType.botChord))
            members.append(Member(4 * i, min(4 * i + 4, nNodes - 1), MemberType.topChord))
            members.append(Member(4 * i, 4 * i + 2, MemberType.diaWeb))
            # right side
            members.append(Member(4 * i - 1, 4 * i + 1, MemberType.vertWeb))
            members.append(Member(4 * i - 1, min(4 * i + 3, nNodes - 2), MemberType.botChord))
            members.append(Member(4 * i + 1, min(4 * i + 5, nNodes - 1), MemberType.topChord))
            members.append(Member(4 * i + 1, min(4 * i + 3, nNodes - 2), MemberType.diaWeb))

    # left to right
    def getTopNodesIndices(self):
        nNodes = self.getNNodes()
        topNodeIndices = []
        for i in range(self.nWeb + 1):
            topNodeIndices.append(4 * i)
        for i in range(self.nWeb + 2):
            topNodeIndices.append(min(4 * (self.nWeb - i) + 5, nNodes - 1))
        return topNodeIndices

    # left to right
    def getBotNodesIndices(self):
        botNodeIndices = []
        for i in range(self.nWeb + 2):
            botNodeIndices.append(max(0, 4 * i - 2))
        for i in range(self.nWeb + 1):
            botNodeIndices.append(max(1, (self.nWeb - i) * 4 - 1))
        return botNodeIndices

    # left to right
    def getTopWebNodesIndices(self):
        topWebNodeIndices = self.getTopNodesIndices()
        removeNodes = [topWebNodeIndices[0],
                       topWebNodeIndices[len(topWebNodeIndices) // 2],
                       topWebNodeIndices[len(topWebNodeIndices) - 1]]

        for i in removeNodes:
            topWebNodeIndices.remove(i)

    # left to right
    def getBotWebNodesIndices(self):
        botWebNodeIndices = self.getBotNodesIndices()
        removeNodes = [botWebNodeIndices[0],
                       botWebNodeIndices[len(botWebNodeIndices) // 2],
                       botWebNodeIndices[len(botWebNodeIndices) - 1]]

        for i in removeNodes:
            botWebNodeIndices.remove(i)

