"""
"""


class ModelBase(object):

    def __init__(self, id):
        self.id = id


class Group(object):
    """
    """


    def __init__(self, id, name, users=None, memberships=None):
        super(Group, self).__init__(id)
        self.name = name
        self.users = [User(**user) for user in users]
        self.memberships = [Membership(**membership) for membership in
                            memberships]


    def __repr__(self):
        return '<Group: %s>' % self.id

    def __str__(self):
        return '%(name)s (%(id)s)' % self


class User(object):
    
    def __init__(self, id, name):
        super(User, self).__init__(id)
        self.id = id
        self.name = name


class Membership(object):

    def __init__(self, id, project, roles=None):
        super(Membership, self).__init__(id)
        self.project = Project(**project)
        self.roles = [Role(**role) for role in roles]


class Project(object):

    def __init__(self, id, name):
        super(Project, self).__init__(id)
        self.id = id
        self.name = name


class Role(object):

    def __init__(self, id, name):
        super(Role, self).__init__(id)
        self.name = name


class Page(object):

    def __init__(self, limit, offset, total_count):
        self.limit = limit
        self.offset = offset
        self.total_count = total_count
        self.__counter = offset

    @property
    def needs_pagination(self):
        return self.total_count > self.limit


    def next(self):
        self.__counter += self.offset


    @property
    def counter(self):
        return self.__counter
