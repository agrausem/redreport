from datetime import datetime
import os


def load_conf_file(mode='r'):
    conf_file = os.path.join(os.path.expanduser('~'), '.redreport.yml')
    return open(conf_file, mode)


def get_date(date):
    return datetime.strptime(date, '%Y/%m/%d').date()


def dateformat(value):
    return value.strftime('%d/%m/%Y')


def monthformat(value):
    return value.strftime('%B %Y')
