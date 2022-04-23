class Member(object):
    """
    Class to store node indices for the two ends of a linear member.
    """
    def __init__(self, start, end, member_type):
        self.start = start
        self.end = end
        self.member_type = member_type
