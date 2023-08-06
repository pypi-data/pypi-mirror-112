# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['volttron', 'volttron.utils']

package_data = \
{'': ['*']}

install_requires = \
['dateutils>=0.6.12,<0.7.0',
 'gevent==20.6.1',
 'greenlet==0.4.16',
 'tzlocal>=2.1,<3.0',
 'watchdog-gevent>=0.1.1,<0.2.0',
 'zmq>=0.0.0,<0.0.1']

setup_kwargs = {
    'name': 'volttron-utils',
    'version': '0.1.2',
    'description': 'Utility classes and methods for VOLTTRON',
    'long_description': None,
    'author': 'C. Allwardt',
    'author_email': 'craig.allwardt@pnnl.gov',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/VOLTTRON/volttron-utils',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.2,<4.0',
}


setup(**setup_kwargs)
