# -*- coding: utf-8 -*-

"""
"""
    
from optparse import make_option
from yaml import dump

from adama.commandment import BaseOrder
from adama.exceptions import OrderError

from ..util import load_conf_file
from .. import api
from .. import conf

class Order(BaseOrder):
    """ Add a user to a team """

    options = BaseOrder.options + (
        # options for order come here
        # use make_option
        # see http://docs.python.org/library/optparse.html#populating-the-parser
    )

    # this constructs a pretty help for the order
    args = 'team logins'
    description = __doc__
    examples = 'redreport add_to_team dip toto'

    def __init__(self):
        super(Order, self).__init__('redreport', command='redreport')

    def execute(self, *args, **options):

        team_name = args[0]
        logins = args[1:]
        users_id = api.get_users_id(*logins)

        if team_name in conf['teams']:
            team = conf['teams'][team_name]
            for user_id in users_id:
                if user_id not in team:
                    conf['teams'][team_name].append(user_id)
        else:
            conf['teams'][team_name] = users_id

        dump(conf, stream=load_conf_file(mode='w'))
        
        return 0
