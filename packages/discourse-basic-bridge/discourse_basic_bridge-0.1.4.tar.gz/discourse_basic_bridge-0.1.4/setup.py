# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['discourse_basic_bridge']

package_data = \
{'': ['*']}

install_requires = \
['bs4>=0.0.1,<0.0.2',
 'lxml>=4.6.3,<5.0.0',
 'requests>=2.25.1,<3.0.0',
 'urllib3>=1.26.6,<2.0.0']

setup_kwargs = {
    'name': 'discourse-basic-bridge',
    'version': '0.1.4',
    'description': 'Discourse Basic Bridge',
    'long_description': '# Discord Basic Bridge\n\n### Version 0.1.1\n\n### Usage:\n\nNews: \n\n```\nimport discord_basic_bridge as dbb\n\nnapi = dbb.News()\n\nprint(napi.news())\n```',
    'author': 'Krish Yadav',
    'author_email': '7krishyadav@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
