# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['anilistWrapPY', 'anilistWrapPY.Anime', 'anilistWrapPY.Media']

package_data = \
{'': ['*']}

install_requires = \
['httpx>=0.18.2,<0.19.0']

setup_kwargs = {
    'name': 'anilistwrappy',
    'version': '0.0.2',
    'description': 'An API Wrapper for Official Anilist.co GraphQL API',
    'long_description': None,
    'author': 'Sayan Biswas',
    'author_email': 'sayan@pokurt.me',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
