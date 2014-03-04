"""
"""

class Pagination(object):
    """
    """

    def __init__(self, limit, offset, total_count):
        self.limit = limit
        self.offset = offset
        self.total_count = total_count


class Group(object):
    """
    """
    
    def __init__(self, id, name, **kwargs):
        self.id = id
        self.name = name

