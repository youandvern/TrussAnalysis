from TrussAnalysis.TrussUtilities.MemberType import MemberType
from TrussAnalysis.TrussUtilities.Node import Node
from TrussAnalysis.TrussUtilities.Member import Member


class Geometry(object):
    """
    Class to generate nodes and members for Parallel Chord Roof Truss geometry
    """
    def __init__(self, span, height, nVertWebsPerSide=1, heightChord=None):
        self.span = span
        self.height = height
        self.heightChord = span / 10 if heightChord is None else heightChord
        self.nWeb = nVertWebsPerSide

    def getNNodes(self):
        return 2 * self.nWeb + 4

    def getNMembers(self):
        return 4 * self.nWeb + 5

    def getPitch(self):
        return self.height / self.span

    def getNodes(self):
        nNodes = self.getNNodes()
        nSpansTop = (2 * (self.nWeb // 2 + 1))
        nSpansBot = (2 * ((self.nWeb + 1) // 2))
        horSpacingTop = self.span / nSpansTop
        horSpacingBot = self.span / nSpansBot
        nodes = []

        # add upper nodes
        for i in range(0, nSpansTop + 1):
            xit = horSpacingTop * i
            hit = min(xit * 2 * self.height / self.span, 2 * self.height - xit * 2 * self.height / self.span) + self.heightChord
            nodes.append(Node(xit, hit))

        # add lower nodes
        for i in range(0, nSpansBot + 1):
            xib = horSpacingBot * i
            hib = min(xib * 2 * self.height / self.span, 2 * self.height - xib * 2 * self.height / self.span)
            nodes.append(Node(xib, hib))

        # sort nodes
        nodes.sort(key=lambda x: (x.x, x.y))

        nodes[0].fixity = 'pin'  # left support
        nodes[-2].fixity = 'roller'  # right support

        return nodes

    def getMembers(self):
        even = (self.nWeb % 2) == 0
        nNodes = self.getNNodes()
        members = []

        if even:
            start = 1
            end = 2
            for i in range(nNodes // 2):
                members.append(Member(start, end, MemberType.topChord))
                start = end
                end += 1 if start == nNodes / 2 else 2

            start = 0
            end = 3
            for i in range(nNodes // 2 - 2):
                members.append(Member(start, end, MemberType.botChord))
                start = end
                end += 3 if start == nNodes / 2 - 1 else 2

            start = 0
            end = 1
            vertWebs = [1, nNodes / 2, nNodes - 1]
            for i in range(nNodes - 1):
                webType = MemberType.vertWeb if end in vertWebs else MemberType.diaWeb
                members.append(Member(start, end, webType))
                start = start if end == 1 or end == nNodes / 2 else end
                end += 1

        else:
            for i in range(1, nNodes - 2, 2):
                members.append(Member(i, i + 2, MemberType.topChord))

            for i in range(0, nNodes - 3, 2):
                members.append(Member(i, i + 2, MemberType.botChord))

            start = 0
            end = 1
            vertWebs = [1, nNodes / 2, nNodes - 2]
            for i in range(nNodes - 1):
                webType = MemberType.vertWeb if end in vertWebs else MemberType.diaWeb
                members.append((Member(start, end, webType)))
                start = start if end == nNodes / 2 else end
                if end < nNodes / 2:
                    end += 1
                elif end == nNodes / 2:
                    end += 2
                elif (end % 2) == 0:
                    end += 3
                else:
                    end -= 1

        return members

    # left to right
    def getTopNodesIndices(self):
        even = (self.nWeb % 2) == 0
        nNodes = self.getNNodes()
        topNodeIndices = []
        topNodeIndices.append(1)

        if even:
            end = 2
            for i in range(nNodes // 2):
                topNodeIndices.append(end)
                end += 1 if end == nNodes / 2 else 2

        else:
            for i in range(3, nNodes, 2):
                topNodeIndices.append(i)

        return topNodeIndices

    # left to right
    def getBotNodesIndices(self):
        even = (self.nWeb % 2) == 0
        nNodes = self.getNNodes()
        botNodeIndices = []
        botNodeIndices.append(0)

        if even:
            end = 3
            for i in range(nNodes // 2 - 2):
                botNodeIndices.append(end)
                end += 3 if end == nNodes / 2 - 1 else 2

        else:
            for i in range(2, nNodes - 1, 2):
                botNodeIndices.append(i)

        return botNodeIndices

    # left to right
    def getTopWebNodesIndices(self):
        return self.getTopNodesIndices()

    # left to right
    def getBotWebNodesIndices(self):
        botWebNodeIndices = self.getBotNodesIndices()
        removeNodes = [botWebNodeIndices[0],
                       botWebNodeIndices[- 1]]

        for i in removeNodes:
            botWebNodeIndices.remove(i)

        return botWebNodeIndices

