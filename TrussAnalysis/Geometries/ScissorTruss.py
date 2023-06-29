from TrussAnalysis.TrussUtilities.MemberType import MemberType
from TrussAnalysis.TrussUtilities.Node import Node
from TrussAnalysis.TrussUtilities.Member import Member


class Geometry(object):
    """
    Class to generate nodes and members for Parallel Chord Roof Truss geometry
    """
    def __init__(self, span, height, nVertWebsPerSide=1, trussDepth=None):
        self.span = span
        self.height = height
        self.trussDepth = span / 8 if trussDepth is None else trussDepth
        self.nWeb = nVertWebsPerSide

    def getNNodes(self):
        return 2 * self.nWeb + 4

    def getNMembers(self):
        return 4 * self.nWeb + 5

    def getPitch(self):
        return self.height / self.span

    def getNodes(self):

        # special geometry when nWeb = 1
        if self.nWeb == 1 and self.height > self.trussDepth > 0:
            mid_x = self.span * (self.height - self.trussDepth) / (2 * self.height - self.trussDepth)
            mid_y = (self.height - self.trussDepth) * (1 + self.trussDepth / (2 * self.height - self.trussDepth))
            return [
                Node(0, 0, "pin"),
                Node(mid_x, mid_y),
                Node(self.span / 2, self.height - self.trussDepth),
                Node(self.span / 2, self.height),
                Node(self.span - mid_x, mid_y),
                Node(self.span, 0, "roller"),
            ]

        nSpans = 2 * (self.nWeb + 1)
        horSpacing = self.span / nSpans
        nodes = []

        is_top = (self.nWeb % 2) == 0
        for i in range(0, nSpans + 1):
            chord_rise = self.height if is_top else self.height - self.trussDepth
            xi = i * horSpacing
            yi = min(xi * 2 * chord_rise / self.span, 2 * chord_rise - xi * 2 * chord_rise / self.span)
            nodes.append(Node(xi, yi))

            # two nodes added at center point
            if i == nSpans / 2:
                nodes.append(Node(xi, self.height))

            is_top = not is_top

        nodes[0].fixity = 'pin'  # left support
        nodes[-1].fixity = 'roller'  # right support

        return nodes

    def getMembers(self):
        even = (self.nWeb % 2) == 0
        nNodes = self.getNNodes()
        members = []

        start = 0
        end = 2 if even else 1
        while start < nNodes - 1:
            members.append(Member(start, min(nNodes - 1, end), MemberType.topChord))
            start = end
            end += 1 if end == nNodes / 2 else 2

        start = 0
        end = 1 if even else 2
        while start < nNodes - 1:
            members.append(Member(start, min(nNodes - 1, end), MemberType.botChord))
            start = end
            end += 3 if end == nNodes / 2 - 1 else 2

        start = 1
        end = 2
        while end <= nNodes - 2:
            members.append(Member(start, end, MemberType.vertWeb if end == nNodes / 2 else MemberType.diaWeb))
            start = start if end == nNodes / 2 else end
            end += 1

        return members

    # left to right
    def getTopNodesIndices(self):
        even = (self.nWeb % 2) == 0
        nNodes = self.getNNodes()
        topNodeIndices = []
        topNodeIndices.append(0)

        i = 2 if even else 1
        for j in range(0, 2 * ((self.nWeb + 1) // 2) + 1):
            topNodeIndices.append(i)
            i += 1 if i == nNodes / 2 else 2

        topNodeIndices.append(nNodes - 1)

        return topNodeIndices

    # left to right
    def getBotNodesIndices(self):
        even = (self.nWeb % 2) == 0
        nNodes = self.getNNodes()
        botNodeIndices = []
        botNodeIndices.append(0)

        i = 1 if even else 2
        for j in range(0, 2 * (self.nWeb // 2) + 1):
            botNodeIndices.append(i)
            i += 3 if i == nNodes / 2 - 1 else 2

        botNodeIndices.append(nNodes - 1)

        return botNodeIndices

    # left to right
    def getTopWebNodesIndices(self):
        topWebNodeIndices = self.getTopNodesIndices()
        removeNodes = [topWebNodeIndices[0],
                       topWebNodeIndices[-1]]

        for i in removeNodes:
            topWebNodeIndices.remove(i)

        return topWebNodeIndices

    # left to right
    def getBotWebNodesIndices(self):
        botWebNodeIndices = self.getBotNodesIndices()
        removeNodes = [botWebNodeIndices[0],
                       botWebNodeIndices[-1]]

        for i in removeNodes:
            botWebNodeIndices.remove(i)

        return botWebNodeIndices

