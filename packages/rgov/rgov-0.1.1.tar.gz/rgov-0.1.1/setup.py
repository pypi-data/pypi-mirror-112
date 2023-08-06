# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rgov', 'rgov.commands']

package_data = \
{'': ['*']}

install_requires = \
['cleo>=0.8.1,<0.9.0',
 'fake-useragent>=0.1.11,<0.2.0',
 'python-daemon>=2.3.0,<3.0.0',
 'requests>=2.25.1,<3.0.0']

entry_points = \
{'console_scripts': ['rgov = rgov.application:main']}

setup_kwargs = {
    'name': 'rgov',
    'version': '0.1.1',
    'description': '',
    'long_description': None,
    'author': 'Jordan Sweet',
    'author_email': 'jsbmgcontact@protonmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
