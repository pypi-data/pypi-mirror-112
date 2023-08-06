# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['volttron',
 'volttron.client',
 'volttron.client.messaging',
 'volttron.client.vip',
 'volttron.client.vip.agent',
 'volttron.client.vip.agent.subsystems']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=5,<6',
 'dateutils>=0.6,<0.7',
 'gevent==20.6.1',
 'greenlet==0.4.16',
 'grequests>=0.6.0,<0.7.0',
 'idna>=2.5,<3',
 'psutil>=5.8.0,<6.0.0',
 'pytz>=2019,<2022',
 'toml>=0.10.2,<0.11.0',
 'tzlocal>=2,<3',
 'volttron-utils>=0.2.1,<0.3.0',
 'zmq>=0.0.0,<0.0.1']

extras_require = \
{':python_version < "3.8"': ['importlib-metadata>=1.0,<2.0']}

setup_kwargs = {
    'name': 'volttron-client',
    'version': '0.2.0',
    'description': 'Client for connecting to a volttron server',
    'long_description': None,
    'author': 'C. Allwardt',
    'author_email': 'craig.allwardt@pnnl.gov',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6.2,<4',
}


setup(**setup_kwargs)
