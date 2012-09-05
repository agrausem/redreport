# -*- coding: utf-8 -*-

"""
"""

from optparse import make_option

from adama.commandment import BaseOrder
from adama.exceptions import OrderError


from redreport import api
from redreport import teams

class Order(BaseOrder):
    """ List members of a team """

    options = BaseOrder.options + (
        # options for order come here
        # use make_option
        # see http://docs.python.org/library/optparse.html#populating-the-parser
    )

    # this constructs a pretty help for the order
    args = 'team_name'
    description = __doc__
    examples = 'redreport list_members dip'

    def __init__(self):
        super(Order, self).__init__('redreport', command='redreport')

    def execute(self, *args, **options):
        # the logic of the order comes here
        team = args[0]
        try:
            users_id = teams[team]
        except KeyError:
            raise OrderError(u"Team {0} doesn't exist".format(team), 'list_team')
        else:
            print u"Members of team {0}".format(team)
            for user_id in users_id:
                user = api.get_user_by_id(user_id)
                print u' - {0[firstname]} {0[lastname]}'.format(user)

        return 0
