import spyre
from yaml import load

from .util import load_conf_file

conf = load(load_conf_file())

try:
    spec_func = getattr(spyre, 'new_from_%s' % conf['general']['spec_source'])
    client = spec_func(conf['general']['spec_uri']) 
except Exception as e:
    print(e)
else:
    client.enable('auth.Header', header_name='X-Redmine-API-Key',
        header_value=conf['general']['api_key'])
    client.enable('format.Json')
