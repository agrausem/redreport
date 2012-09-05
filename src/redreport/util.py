from datetime import datetime

def limit_and_offset(function, total, key=""):
    """
    """
    result = []

    offset = total / 100
    limit = offset if total % 100 == 0 else offset + 1
    call_num = 1

    while call_num <= limit:
        response = function(format='json', limit=str(call_num * 100), 
            offset=str((call_num - 1) * 100)).content
        result_tmp = [item for item in response[key]] if key else response
        result.extend(result_tmp)
        call_num += 1

    return result


def get_date(date):
    return datetime.strptime(date, '%Y/%m/%d').date()


def dateformat(value):
    return value.strftime('%d/%m/%Y')


def monthformat(value):
    return value.strftime('%B %Y')
