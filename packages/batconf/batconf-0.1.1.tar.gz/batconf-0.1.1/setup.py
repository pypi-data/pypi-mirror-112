# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['batconf', 'batconf.sources', 'batconf.sources.tests', 'batconf.tests']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=5.4.1,<6.0.0']

setup_kwargs = {
    'name': 'batconf',
    'version': '0.1.1',
    'description': 'Application configuration tool from the BAT project',
    'long_description': None,
    'author': 'Lundy Bernard',
    'author_email': 'lundy.bernard@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
