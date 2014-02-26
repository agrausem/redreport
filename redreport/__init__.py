import britney
from britney.middleware import auth, format
from yaml import load

from .util import load_conf_file

conf = load(load_conf_file())

try:
    client = britney.spyre(conf['general']['spec_uri'],
                           base_url=conf['general']['redmine_url'])
except Exception as e:
    print(e)
else:
    client.enable(format.Json)
    client.enable(auth.ApiKey,
                  key_name='X-Redmine-API-Key',
                  key_value=conf['general']['redmine_key'])
