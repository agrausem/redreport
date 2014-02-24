import os
from jinja2 import Environment
from jinja2 import PackageLoader
from jinja2 import PrefixLoader

from . import conf
from . import util

__template_packages = {'default': PackageLoader('redreport', 'templates')}

for plugin in conf['plugins']:
    try:
        module = __import__(plugin)
    except ImportError:
        pass
    else:
        if os.path.exists(os.path.join(module.__path__), 'templates'):
            __template_packages[plugin] = PackageLoader(plugin, 'templates')

env = Environment(loader=PrefixLoader(__template_packages))
env.filters['dateformat'] = util.dateformat
env.filters['monthformat'] = util.monthformat
