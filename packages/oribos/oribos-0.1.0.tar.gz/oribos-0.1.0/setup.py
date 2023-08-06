# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['oribos']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'oribos',
    'version': '0.1.0',
    'description': 'A sample Python package',
    'long_description': None,
    'author': 'A. Random Developer',
    'author_email': 'author@example.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
