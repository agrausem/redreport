import spyre
import os
from yaml import load
from jinja2 import Environment, PackageLoader

from redreport import util


config_file = os.path.join(os.path.dirname(__path__[0]), 'conf.yml')

config = load(open(config_file, 'r'))
teams = config['teams']
general_conf = config['general']

templates_env = Environment(loader=PackageLoader('redreport', 'templates'))
templates_env.filters['dateformat'] = util.dateformat
templates_env.filters['monthformat'] = util.monthformat

try:
    spec_func = getattr(spyre, 'new_from_%s' % general_conf['spec_source'])
    client = spec_func(general_conf['spec_uri']) 
except Exception as e:
    print(e)
else:
    client.enable('auth.Header', header_name='X-Redmine-API-Key',
        header_value=general_conf['api_key'])
    client.enable('format.Json')
