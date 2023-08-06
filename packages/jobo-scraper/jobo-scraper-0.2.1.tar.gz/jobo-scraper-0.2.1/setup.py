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
    'version': '0.2.1',
    'description': 'Jobo web scraper for get the current available events.',
    'long_description': '# jobo-scraper\n\n[![pypi release](https://img.shields.io/pypi/v/jobo-scraper)](https://pypi.org/project/jobo-scraper/)\n[![codecov](https://codecov.io/gh/Luis-GA/jobo-scrapper/branch/main/graph/badge.svg?token=GJQ1ZB3RRH)](https://codecov.io/gh/Luis-GA/jobo-scrapper)\n\nPython library for scraping the [Jobo webpage](https://madridcultura-jobo.shop.secutix.com/) to search the available events.\n\n## Installation\n\n```sh\n$ pip install jobo-scraper\n```\n\n## Usage\n\n```python\nfrom jobo_scraper import JoboScraping\n\njobo = JoboScraping ("<user>", "<password>")\n\nprint(jobo.get_list_of_events())\n```',
    'author': 'Luis Gómez Alonso',
    'author_email': 'luis.gomez.alonso95@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Luis-GA/jobo-scrapper',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
