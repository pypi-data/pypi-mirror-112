# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ecas']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4>=4.9.3,<5.0.0',
 'click>=8.0.1,<9.0.0',
 'requests>=2.25.1,<3.0.0']

entry_points = \
{'console_scripts': ['ecas = ecas.ecas:list_ecas_steps']}

setup_kwargs = {
    'name': 'ecas',
    'version': '0.1.2a0',
    'description': 'A CLI to directly read your PR status',
    'long_description': '# Ecas RP automation script\nThis tool has been written to check the status of your PR application in ECAS automatically. This avoid multiple click and form filling. You can set alert using a system like cron.\n## Getting started\n### From PyPI\n```bash\npip3 install ecas\n```\n### From Source\n1. Get the code\n\nFirst get this code on your machine with\n```bash\ngit clone git@github.com:pievalentin/ecas.git && cd ecas\n```\n2. Install the tool\n\nRun this command to install the tool:\n```bash\npip3 install .\n```\nRestart your terminal so that `ecas` is available.\n## Usage\n\n```bash\necas lastname iuc_number birthday birth_country_code\n```\n\nFor example for France:\n```bash\necas Dupont 112245589 "2001-01-31" 022\n```\n\nFor more details, you can\n```bash\necas --help\n```\n## Find your country code\n\nTo find your country code, you can look it up [in this file](/country_code.html)\n\n## NB\nUse this tool responsibly. Don\'t spam IRCC server :)\n',
    'author': 'Pierre Valentin',
    'author_email': 'pievalentin@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/pievalentin/ecas',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
