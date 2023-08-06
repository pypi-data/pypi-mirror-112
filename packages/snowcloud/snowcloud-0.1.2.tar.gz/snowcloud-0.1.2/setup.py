# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['snowcloud']

package_data = \
{'': ['*']}

install_requires = \
['Flask>=2.0.1,<3.0.0',
 'gunicorn>=20.1.0,<21.0.0',
 'redis>=3.5.3,<4.0.0',
 'requests>=2.25.1,<3.0.0']

setup_kwargs = {
    'name': 'snowcloud',
    'version': '0.1.2',
    'description': 'Service for generating unique, time-ordered IDs across distributed worker processes.',
    'long_description': None,
    'author': 'Brooke Chalmers',
    'author_email': 'breq@breq.dev',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
