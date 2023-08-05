# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['net_gsd',
 'net_gsd.connections',
 'net_gsd.host',
 'net_gsd.runner',
 'net_gsd.task']

package_data = \
{'': ['*']}

install_requires = \
['asyncssh>=2.7.0,<3.0.0',
 'genie==21.4',
 'pyats==21.4',
 'scrapli>=2021.1.30,<2022.0.0']

setup_kwargs = {
    'name': 'net-gsd',
    'version': '0.1.2',
    'description': 'Network Get Stuff Done',
    'long_description': None,
    'author': 'Ryan Bradshaw',
    'author_email': 'ryan@rbradshaw.dev',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
