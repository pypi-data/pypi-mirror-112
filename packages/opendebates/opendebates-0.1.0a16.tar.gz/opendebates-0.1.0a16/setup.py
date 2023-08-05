# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['opendebates']

package_data = \
{'': ['*']}

install_requires = \
['erin>=0.1.0-alpha.3,<0.2.0']

setup_kwargs = {
    'name': 'opendebates',
    'version': '0.1.0a16',
    'description': 'Rating System Bot for Open Debates Discord Server',
    'long_description': '<h1 align="center">OpenDebates for Discord</h1>\n<p align="center">\n    <a href="https://opendebates.rtfd.io"><img width="100" src="https://i.imgur.com/SxX5wQF.png"/></a>\n</p>\n<p align="center">\n    <br>\n    <br>\n    <a href="https://github.com/OpenDebates/OpenDebates/actions/workflows/main.yml">\n        <img src="https://github.com/OpenDebates/OpenDebates/actions/workflows/main.yml/badge.svg"/>\n    </a>\n    <a href="https://opendebates.readthedocs.io/en/latest/?badge=latest">\n        <img src="https://readthedocs.org/projects/opendebates/badge/?version=latest" alt=\'Documentation Status\'/>\n    </a>\n</p>\n<hr>\n<h4>What is OpenDebates for Discord?</h4>\n    <p>It is a bot for discord, that allows users to participate in debates that are ranked by ELO ratings.</p>\n',
    'author': 'Taven',
    'author_email': 'taven@outlook.in',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://opendebates.net',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
