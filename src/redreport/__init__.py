import spyre
import os
from yaml import load
from jinja2 import Environment, PackageLoader

from redreport import util


config_file = os.path.join(os.path.dirname(__path__[0]), 'conf.yml')

config = load(open(config_file, 'r'))
teams = config['teams']
templates_env = Environment(loader=PackageLoader('redreport', 'templates'))
templates_env.filters['dateformat'] = util.dateformat
templates_env.filters['monthformat'] = util.monthformat

try:
    client = spyre.new_from_spec(
        '/home/arnaud/Projets/reporting/chronos.json',
        'https://chronos.u-strasbg.fr/redmine'
    ) 
except Exception as e:
    print(e)
else:
    client.enable('auth.Header', header_name='X-Redmine-API-Key',
        header_value='8c9602ee1f5de0f7ca5a53c6ca07545ec1ab5cc0')
    client.enable('format.Json')
