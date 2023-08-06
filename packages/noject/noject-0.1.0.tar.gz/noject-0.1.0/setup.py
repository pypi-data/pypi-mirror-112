# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['noject']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'noject',
    'version': '0.1.0',
    'description': 'A pain-free solution for writing in-line SQL safely.',
    'long_description': None,
    'author': 'tlonny',
    'author_email': 't@lonny.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
