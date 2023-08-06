# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['figure_parser',
 'figure_parser.alter',
 'figure_parser.gsc',
 'figure_parser.native']

package_data = \
{'': ['*'], 'figure_parser.gsc': ['locale/*']}

install_requires = \
['PyYAML==5.2',
 'aiohttp>=3.7.4,<4.0.0',
 'beautifulsoup4>=4.9.3',
 'feedparser>=6.0.8,<7.0.0',
 'lxml>=4.6.3',
 'pytz>=2021.1,<2022.0',
 'requests>=2.25.1',
 'toml>=0.10.2,<0.11.0']

setup_kwargs = {
    'name': 'figure-parser',
    'version': '0.0.1',
    'description': 'Parser for figure',
    'long_description': '## Maker List\n|                | Product parser | Delay parser | Shipment parser |\n| -------------- | -------------- | ------------ | --------------- |\n| GSC            | V              |              | V               |\n| Alter          | V              |              |                 |\n| native         | V              |              |                 |\n| SKYTUBE        |                |              |                 |\n| AMAKUNI        |                |              |                 |\n| KOTOBUKIYA     |                |              |                 |\n| daikikougyou   |                |              |                 |\n| OrchidSeed     |                |              |                 |\n| FLARE          |                |              |                 |\n| PLUM           |                |              |                 |\n| WAVE           |                |              |                 |\n| union-creative |                |              |                 |\n| alphamax       |                |              |                 |\n| ORCATORYS      |                |              |                 |\n| quesQ          |                |              |                 |\n| MegaHouse      |                |              |                 |\n\n## Shop List\n- [ ] TokyoFigure\n- [ ] HobbyJapan\n- [ ] amiami\n- [ ] toranoana\n- [ ] melonbooks',
    'author': 'Elton Chou',
    'author_email': 'plscd748@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/FigureHook/figure_parser',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
