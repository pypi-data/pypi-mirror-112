# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['autodrive', 'autodrive.formatting']

package_data = \
{'': ['*']}

install_requires = \
['google-api-python-client-stubs>=1.2.0,<2.0.0',
 'google-api-python-client>=2.0.2,<3.0.0',
 'google-auth-httplib2>=0.1.0,<0.2.0',
 'google-auth-oauthlib>=0.4.3,<0.5.0',
 'jsonlines>=2.0.0,<3.0.0',
 'pandas>=1.2.3,<2.0.0']

setup_kwargs = {
    'name': 'autodrive',
    'version': '0.1.0',
    'description': 'A simple python library with tools for reading, writing, and formatting Google Sheets via the Google API.',
    'long_description': None,
    'author': 'Chris Larabee',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
