# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['wikiusers_cli', 'wikiusers_cli.utils']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0.1,<9.0.0',
 'prompt-toolkit==1.0.14',
 'whaaaaat>=0.5.2,<0.6.0',
 'wikiusers>=1.0.0,<2.0.0']

entry_points = \
{'console_scripts': ['wikiusers = wikiusers_cli:run']}

setup_kwargs = {
    'name': 'wikiusers-cli',
    'version': '1.1.0',
    'description': 'The cli of the wikiusers python module',
    'long_description': None,
    'author': 'Eugenio Vinicio Berretta',
    'author_email': 'euberdeveloper@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
