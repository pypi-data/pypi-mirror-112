# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['peodd', 'tests']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.0,<8.0', 'release-tools>=0.3.0,<0.4.0', 'tomlkit>=0.5.8,<0.6.0']

entry_points = \
{'console_scripts': ['peodd = peodd.peodd:main']}

setup_kwargs = {
    'name': 'peodd',
    'version': '0.1.0',
    'description': 'Script to export the pyproject.toml dev-dependencies to a txt file.',
    'long_description': '# peodd\npoetry export, but only for dev-dependencies\n',
    'author': 'Venu Vardhan Reddy Tekula',
    'author_email': 'venuvardhanreddytekula8@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/vchrombie/peodd',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
