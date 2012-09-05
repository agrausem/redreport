# -*- coding: utf-8 -*-

"""
"""

from optparse import make_option

from adama.commandment import BaseOrder
from adama.exceptions import OrderError
import isoweek
import calendar
from datetime import date

from redreport import api
from redreport import util
from redreport import teams
from redreport import templates_env

class Order(BaseOrder):
    """ Constructs a per user report """

    options = BaseOrder.options + (
        make_option("-t", "--team", action="store", type="string",
            dest="team"),
        make_option("-w", "--week", action="store", type="int", dest="week",
            default=isoweek.Week.thisweek().week),
        make_option("-y", "--year", action="store", type="int", dest="year",
            default=date.today().year),
        make_option("-m", "--month", action="store", type="int", dest="month"),
        make_option("-e", action="store", type="string", dest="end"),
        make_option("-b", action="store", type="string", dest="begin")
        # options for order come here
        # use make_option
        # see http://docs.python.org/library/optparse.html#populating-the-parser
    )

    # this constructs a pretty help for the order
    args = ''
    description = __doc__
    examples = 'chronos per_user -t dip 29 -b 2012/06/01 -e 2012/06/08'


    def __init__(self):
        super(Order, self).__init__('redreport', command='redreport')

    def execute(self, *args, **options):
        begin, end = options['begin'], options['end']
        report = ""
        if all([begin, end]):
            begin = util.get_date(begin)
            end = util.get_date(end)
        else:
            if any([begin, end]):
                raise OrderError(
                    'You should specify a begin and an end date !',
                    'per_user')
            if options['month']:
                report = 'month'
                begin = date(options['year'], options['month'], 1)
                end = date(options['year'], options['month'],
                           calendar.monthrange(options['year'],
                                               options['month'])[1])
            else:
                report = "week"
                week = isoweek.Week(options['year'], options['week'])
                begin = week.day(0)
                end = week.day(6)

        if options['team'] is not None:
            try:
                team = teams[options['team']]
            except KeyError:
                raise OrderError('Team {0} doesn\'t exist'.format(
                    options['team']) , 'per_user')
        else:
            team = None
        
        time_entries = api.get_time_entries(week.day(0), week.day(6), team)
        users = {}
        for user in api.get_users(team):
            users[user['id']] = user

        per_user = {}
        for time_entry in time_entries:
            if time_entry['user']['id'] not in per_user:
                per_user[time_entry['user']['id']] = float(time_entry['hours'])
            else:
                per_user[time_entry['user']['id']] += float(time_entry['hours'])

        template = templates_env.get_template('per_user.temp')
        print template.render(report=report, week=week, begin=begin, end=end,
            per_user_items=per_user.items(), total=sum(per_user.values()),
            users=users)

        return 0
