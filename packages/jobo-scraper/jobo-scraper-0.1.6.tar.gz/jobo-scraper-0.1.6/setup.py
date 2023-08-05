# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['jobo_scraper']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4>=4.9.3,<5.0.0', 'requests>=2.25.1,<3.0.0']

setup_kwargs = {
    'name': 'jobo-scraper',
    'version': '0.1.6',
    'description': 'Jobo web scraper for get the current available events.',
    'long_description': None,
    'author': 'Luis Gómez Alonso',
    'author_email': 'luis.gomez.alonso95@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
