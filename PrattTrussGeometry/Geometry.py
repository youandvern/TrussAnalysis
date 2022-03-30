from PrattTrussGeometry import MemberType
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

    def getNodes(self):
        nNodes = 4*self.nWeb + 4
        horSpacing = self.span / (2*nNodes+2)
        nodes = []
        nodes.append(Node(0, 0, fixity='pin'))  # left support
        nodes.append(Node(self.span, 0, fixity='roller'))  # right support

        for i in range(1, self.nWeb):
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
        members = []
        # left 2, right 2
        for i in range(1, self.nWeb):
            members.append(Member(0, 1, MemberType.botChord))  # webs + chords
        # center




