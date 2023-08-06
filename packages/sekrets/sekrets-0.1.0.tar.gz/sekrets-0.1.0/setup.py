# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sekrets']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'sekrets',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Alexander Bausk',
    'author_email': 'bauskas@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
