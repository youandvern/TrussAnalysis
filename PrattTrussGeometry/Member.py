class Member(object):
    """
    Class to store node indices for the two ends of a linear member.
    """
    def __init__(self, start, end, type):
        self.start = start
        self.end = end
        self.type = type
