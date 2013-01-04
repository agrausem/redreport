
from . import api

def get_per_projects(time_entries):
    per_project = {}
    for time_entry in time_entries:
        project_name = time_entry['project']['name']
        if project_name not in per_project:
            per_project[project_name] = {
                'time': float(time_entry['hours']),
                'id': time_entry['project']['id'],
                'activities': {
                    time_entry['activity']['id']: {
                        'time': float(time_entry['hours']),
                        'name': time_entry['activity']['name']
                    }
                }
            }
        else:
            per_project[project_name]['time'] += float(time_entry['hours'])
            activity_id = time_entry['activity']['id']
            if activity_id not in per_project[project_name]['activities']:
                per_project[project_name]['activities'][activity_id] = {
                    'time': float(time_entry['hours']),
                    'name': time_entry['activity']['name']
                }
            else:
                per_project[project_name]['activities'][activity_id]['time'] += \
                        float(time_entry['hours'])

    return per_project


def get_per_base_projects(time_entries):

    per_project = get_per_projects(time_entries)

    per_project_group = {}
    for project_name, project_data in per_project.items():
        parent = api.get_parent_project(project_data['id'], base_projects=True)
        if parent['name'] not in per_project_group:
            per_project_group[parent['name']] = {
                'projects': [{project_name: project_data['time']}],
                'time': float(project_data['time']),
                'activities': project_data['activities'],
                'id': parent['id']
            }
        else:
            per_project_group[parent['name']]['time'] += float(
                project_data['time'])
            per_project_group[parent['name']]['projects'].append(
                {project_name: project_data['time']})
            for activity in project_data['activities'].keys():
                if activity in per_project_group[parent['name']]['activities']:
                    per_project_group[parent['name']]['activities'][activity]['time'] += \
                        project_data['activities'][activity]['time']
                else:
                    per_project_group[parent['name']]['activities'][activity] = \
                        project_data['activities'][activity]

    return per_project_group


def get_special_base_projects_report(time_entries):

    per_project_group = get_per_base_projects(time_entries)

    special_report = {}
    for project_group, data in per_project_group.items():
        if api.is_a_special_projects_group(data['id']):
            special_group = api.get_special_projects_group(data['id'])
            print special_group
            for project, group_data in special_group.items():
                if project not in special_report:
                    special_report[project] = sum([
                        data['activities'][activity]['time'] for activity in
                        data['activities'] if int(activity) in group_data['activities']
                    ])
                else:
                    special_report[project] += sum([
                        data['activities'][activity]['time'] for activity in
                        data['activities'] if int(activity) in group_data['activities']
                    ])

        else:
            special_report[api.conf['base_projects'][data['id']]['display']] = \
                data['time']

    return special_report
