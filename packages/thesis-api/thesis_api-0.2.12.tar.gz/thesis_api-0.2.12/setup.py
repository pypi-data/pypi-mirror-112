# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['thesis_api', 'thesis_api.tools']

package_data = \
{'': ['*'], 'thesis_api.tools': ['templates/*']}

setup_kwargs = {
    'name': 'thesis-api',
    'version': '0.2.12',
    'description': '',
    'long_description': None,
    'author': 'Julian Stang',
    'author_email': 'julian.stang@tum.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
