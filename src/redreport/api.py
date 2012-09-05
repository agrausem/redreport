from redreport import client
from redreport.util import get_date


def count_elements(function):
    response = function(format='json', limit='1')
    return int(response.content['total_count'])


def get_users(team=None):

    users = []

    total_users = count_elements(client.list_users)
    limit = total_users / 100
    if total_users % 100 != 0:
        limit += 1

    call_num = 1
    while call_num <= limit:
        response = client.list_users(format='json', limit=str(call_num * 100),
                   offset=str((call_num - 1) * 100))

        if team:
            users_partial = [user for user in response.content['users']
                if user['id'] in team]
        else:
            users_partial = response.content['users']
        users.extend(users_partial)
        
        if team and len(users) == len(team):
            break

        call_num += 1

    return users


def get_user_by_id(user_id):
    return client.get_user(format='json', id=str(user_id)).content['user']


def get_users_id(team=None):
    return [user['id'] for user in get_users(team)]


def get_project_by_id(project_id):
    return client.get_project(format='json',
            id=str(project_id)).content['project']


def get_parent_project(project_id, last=False):
    """
    """
    project = get_project_by_id(project_id)
    if last:
        while 'parent' in project:
            project = get_project_by_id(project['parent']['id'])
        return project
    elif 'parent' in project:
        return get_project_by_id(project['parent']['id'])
    return None


def get_time_entries(begin, end, team=None):
    """
    """
    time_entries = []

    users_id = get_users_id(team)
    
    total_time_entries = count_elements(client.list_time_entries)
    limit = total_time_entries / 100
    if total_time_entries % 100 != 0:
        limit +=1
    
    call_num = 1
    while call_num <= limit:
        call_num += 1

        response = client.list_time_entries(format='json', 
                                           limit=str(call_num * 100),
                                           offset=str((call_num - 1) * 100))

        time_entries_partial = response.content['time_entries']
        if get_date(time_entries_partial[0]['spent_on']) < begin:
            break
        if get_date(time_entries_partial[-1]['spent_on']) > end:
            continue

        time_partial = [time_entry for time_entry in time_entries_partial
                if begin <= get_date(time_entry['spent_on']) <= end \
                    and time_entry['user']['id'] in users_id]
        
        time_entries.extend(time_partial)

    return time_entries
