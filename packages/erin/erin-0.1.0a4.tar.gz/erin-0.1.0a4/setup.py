# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['erin', 'erin.cli', 'erin.core', 'erin.db', 'erin.db.drivers']

package_data = \
{'': ['*']}

install_requires = \
['certifi>=2021.5.30,<2022.0.0',
 'cookiecutter>=1.7.3,<2.0.0',
 'discord.py>=1.7.3,<2.0.0',
 'dnspython>=2.1.0,<3.0.0',
 'motor>=2.4.0,<3.0.0',
 'schema>=0.7.4,<0.8.0',
 'toml>=0.10.2,<0.11.0',
 'verboselogs>=1.7,<2.0']

entry_points = \
{'console_scripts': ['erin = erin.__main__:main']}

setup_kwargs = {
    'name': 'erin',
    'version': '0.1.0a4',
    'description': 'Fully Fledged Discord Bot Framework',
    'long_description': '<h1 align="center">Erin</h1>\n<p align="center">\n    <a href="https://erin.rtfd.io"><img width="100" src="https://i.imgur.com/GK2KgOe.gif"/></a>\n</p>\n<p align="center">\n    Batteries Included\n    <br>\n    <br>\n    <a href="https://github.com/OpenDebates/Erin/actions/workflows/main.yml">\n        <img src="https://github.com/OpenDebates/Erin/actions/workflows/main.yml/badge.svg"/>\n    </a>\n    <a href="https://codeclimate.com/github/OpenDebates/Erin/maintainability">\n        <img src="https://api.codeclimate.com/v1/badges/e5ea00ded93f855cb5a4/maintainability"/>\n    </a>\n    <a href="https://codecov.io/gh/OpenDebates/Erin">\n        <img src="https://codecov.io/gh/OpenDebates/Erin/branch/master/graph/badge.svg"/>\n    </a>\n    <a href="https://erin.readthedocs.io/en/latest/?badge=latest">\n        <img src="https://readthedocs.org/projects/erin/badge/?version=latest" alt=\'Documentation Status\'/>\n    </a>\n</p>\n<hr>\n<h4>What is Erin?</h4>\n    <p>Erin is an initiative to build a bot development framework like how flask is a framework for web applications. It is built on top of the <a href="https://github.com/Rapptz/discord.py">discord.py</a> library and supports all of it\'s extensions by default.</p>\n\n<h4>Can I get started with Erin today?</h4>\n   <p>Yes, Erin works out of the box with all <a href="https://github.com/Rapptz/discord.py">discord.py</a> <a href="https://discordpy.readthedocs.io/en/stable/ext/commands/api.html#discord.ext.commands.Bot.load_extension">extensions</a>. You can read how to set it up in the <a href="https://erin.readthedocs.io/en/latest/?badge=latest">documentation</a>. However, keep in mind that this project has not even released a pre-alpha yet. This is because we are still deliberating core architecture and we want to get it right the first time. As a result expect plenty of changes to the API without any notice at all.</p>\n\n',
    'author': 'Taven',
    'author_email': 'taven@outlook.in',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/OpenDebates/Erin',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
