# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['peodd', 'tests']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.0,<8.0', 'release-tools>=0.3.0,<0.4.0', 'tomli>=1.0.4,<2.0.0']

entry_points = \
{'console_scripts': ['peodd = peodd.peodd:main']}

setup_kwargs = {
    'name': 'peodd',
    'version': '0.2.0',
    'description': 'Script to export the pyproject.toml dev-dependencies to a txt file.',
    'long_description': "# peodd\n\npoetry export, but only for dev-dependencies\n\nScript to export the pyproject.toml dev-dependencies to a txt file.\n\nThis software is licensed under GPL3 or later.\n\n**Note:** Right now, this tool supports only some poetry formats of the dependencies (specifically `foo = '^n.n.n'`, `foo = '>=n.n.n'`, `foo = 'n.n.n'`). I would be interested to add support for more formats, please [open an issue](https://github.com/vchrombie/peodd/issues/new) incase if you need any other. \n\n## Requirements\n\n * Python >= 3.6\n * Poetry >= 1.0\n * tomlkit >= 0.5.8\n * Click >= 7.0.0\n * release-tools >= 0.3.0\n\n## Installation\n\n### PyPI\n\nYou can install the package directly using pip.\n```\n$ pip install peodd\n```\n\n### Getting the source code\n\nClone the repository\n```\n$ git clone https://github.com/vchrombie/peodd/\n$ cd peodd/\n```\n\n### Prerequisites\n\n#### Poetry\n\nWe use [Poetry](https://python-poetry.org/docs/) for managing the project.\nYou can install it following [these steps](https://python-poetry.org/docs/#installation).\n\nWe use [Bitergia/release-tools](https://github.com/Bitergia/release-tools) for managing \nthe releases. This is also used in the project, so you need not install it again.\n\n### Installation\n\nInstall the required dependencies (this will also create a virtual environment)\n```\n$ poetry install\n```\n\nActivate the virtual environment\n```\n$ poetry shell\n```\n\n## Usage\n\nOnce you install the tool, you can use it with the `peodd` command.\n```\n$ peodd --help\nUsage: peodd [OPTIONS]\n\n  Script to export the pyproject.toml dev-dependencies to a txt file.\n\nOptions:\n  -o, --output TEXT  Output file for the dependencies  [default: requirements-\n                     dev.txt]\n\n  --help             Show this message and exit.\n```\n\nExport the dev-dependencies to `requirements-dev.txt` file\n```\n$ peodd -o requirements-dev.txt\n```\n\n## Contributions\n\nAll contributions are welcome. Please feel free to open an issue or a PR. \nIf you are opening any PR for the code, please be sure to add a \n[changelog](https://github.com/Bitergia/release-tools#changelog) entry.\n\n## License\n\nLicensed under GNU General Public License (GPL), version 3 or later.\n",
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
