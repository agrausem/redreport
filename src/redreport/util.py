from datetime import datetime


def get_date(date):
    return datetime.strptime(date, '%Y/%m/%d').date()


def dateformat(value):
    return value.strftime('%d/%m/%Y')


def monthformat(value):
    return value.strftime('%B %Y')
