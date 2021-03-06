"""
"""

from redreport import conf
from redreport import client
from redreport.util import get_date
import re

BASE_PROJECTS_ID = [] # conf['base_projects'].keys()


def get_pagination_for(func, **kwargs):
    response = func(**kwargs)
    if response.paginate and response.paginate.needs_pagination:
        paginate = response.paginate
        while paginate.counter < paginate.total_count:
            response_tmp = func(**kwargs.update({'offset': paginate.counter}))
            response.objects.append(response_tmp.objects)
            paginate.next()


def get_group(id):
    """ Get a redmine group with his id

    :param id: id of the group to search
    :rtype: a Group object
    """

    response = client.get_group(id=str(id), include="users,memberships")
    return response.object


def get_groups_by_name(name):
    """ Get a redmine group with it's members

    :param name: name of the group
    :type name: can be a partial name or a regex)
    :rtype: a dict
    """
    response = get_pagination_for(client.list_groups)
    return [
        get_group(group.id) for group in response.objects
        if re.search(name, group.name, re.I)
    ]


def count_elements(function):
    """
    Count elements returned by a Redmine API Rest URI call
    
    :param function: a WS-API function to call 
    :type function: function
    :rtype: an integer
    """
    response = function(format='json', limit='1')
    return int(response.content['total_count'])


def get_users(*identifiers):
    """
    Get users from Redmine

    :param team: ididentifiers of users
    :type team: list of identifiers or usernames
    :rtype: a JSON list of Redmine users
    """

    users = []

    total_users = count_elements(client.list_users)
    limit = total_users / 100
    if total_users % 100 != 0:
        limit += 1

    call_num = 1
    while call_num <= limit:
        response = client.list_users(format='json', limit=str(call_num * 100),
                   offset=str((call_num - 1) * 100))

        if identifiers:
            users_partial = [user for user in response.content['users']
                if user['id'] in identifiers or user['login'] in identifiers]
        else:
            users_partial = response.content['users']
        users.extend(users_partial)
        
        if identifiers and len(users) == len(identifiers):
            break

        call_num += 1

    return users


def get_user_by_id(user_id):
    """ Get a user from his Redmine id

    :param user_id: the Redmine user id
    :type users_id: an integer
    :rtype: a JSON formatted Redmine user
    """
    return client.get_user(format='json', id=str(user_id)).content['user']


def get_users_id(*logins):
    """ Get a list of users Redmine id

    :param logins: Redmine usernames
    :type logins: strings
    :rtype: list of Redmine user ids
    """
    return [user['id'] for user in get_users(*logins)]


def get_project_by_id(project_id):
    """ Get a Redmine project with his id

    :param project_id: id of Redmine project
    """
    return client.get_project(format='json',
            id=str(project_id)).content['project']


def get_parent_project(project_id, last=False, base_projects=False):
    """
    """
    project = get_project_by_id(project_id)
    if last:
        while 'parent' in project:
            project = get_project_by_id(project['parent']['id'])
        return project
    elif base_projects:
        while project['id'] not in BASE_PROJECTS_ID:
            project = get_project_by_id(project['parent']['id'])
        return project
    elif 'parent' in project:
        return get_project_by_id(project['parent']['id'])
    return None


def get_time_entries(begin, end, team=None):
    """
    """
    time_entries = []

    users_id = get_users_id(*team)
    
    total_time_entries = count_elements(client.list_time_entries)
    limit = total_time_entries / 100
    if total_time_entries % 100 != 0:
        limit +=1
    
    call_num = 0
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


def get_man_days(hours):
    """
    Gets the time in days.man
    :param hours: hours to convert
    :type hours: float
    :rtype: 1 rounded float
    """
    return round(hours / 7.3, 2)


def is_a_special_projects_group(project_id):
    """
    """
    return conf['base_projects'][project_id]['special']


def get_special_projects_group(project_id):
    """
    """
    project = conf['base_projects'][project_id]['name']
    return conf[project]
