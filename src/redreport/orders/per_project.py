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
    """ Construct a per project and team report """

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
                    'per_project')
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
                    options['team']) , 'per_project')
        else:
            team = None

        time_entries = api.get_time_entries(begin, end, team)

        per_project = {}
        for time_entry in time_entries:
            project_name = time_entry['project']['name']
            if project_name not in per_project:
                per_project[project_name] = {
                        'time': float(time_entry['hours']),
                        'id': time_entry['project']['id']}
            else:
                per_project[project_name]['time'] += float(time_entry['hours'])

        per_project_group = {}
        for project_name, project_data in per_project.items():
            parent = api.get_parent_project(project_data['id'], last=True)
            if parent['name'] not in per_project_group:
                per_project_group[parent['name']] = {
                        'projects': [{project_name: project_data['time']}],
                        'time': float(project_data['time'])}
            else:
                per_project_group[parent['name']]['time'] += float(project_data['time'])
                per_project_group[parent['name']]['projects'].append({project_name: project_data['time']})

        template = templates_env.get_template('per_project.temp')
        print template.render(report=report, week=week, begin=begin, end=end,
            per_project_group_items=per_project_group.items(),
            total=sum(data['time'] for data in per_project_group.values()))

        return 0
