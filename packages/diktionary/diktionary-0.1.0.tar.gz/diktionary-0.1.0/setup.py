# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['diktionary']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'diktionary',
    'version': '0.1.0',
    'description': 'Simple, zero-deps recursive default dictionary',
    'long_description': None,
    'author': 'Gilad Barnea',
    'author_email': 'cr-gbarn-herolo@allot.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
