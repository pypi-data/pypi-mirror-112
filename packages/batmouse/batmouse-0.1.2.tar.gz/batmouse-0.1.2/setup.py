# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['batmouse']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'batmouse',
    'version': '0.1.2',
    'description': 'Python library for querying mouse battery levels.',
    'long_description': None,
    'author': 'Tarcísio Eduardo Moreira Crocomo',
    'author_email': 'tarcisioe@pm.me',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
