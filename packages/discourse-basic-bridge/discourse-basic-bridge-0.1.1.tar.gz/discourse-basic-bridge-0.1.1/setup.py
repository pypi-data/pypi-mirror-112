# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['discourse_basic_bridge']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'discourse-basic-bridge',
    'version': '0.1.1',
    'description': '',
    'long_description': None,
    'author': 'Krish Yadav Team leader',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
