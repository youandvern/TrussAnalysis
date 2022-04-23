class Node(object):
    """
    Class to store geometry and fixity data of a node.
    """
    def __init__(self, x, y, fixity='free'):
        self.x = x
        self.y = y
        self.fixity = fixity
