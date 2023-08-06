# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['codefind']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'codefind',
    'version': '0.1.1',
    'description': 'Find code objects and their referents',
    'long_description': None,
    'author': 'Olivier Breuleux',
    'author_email': 'breuleux@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
