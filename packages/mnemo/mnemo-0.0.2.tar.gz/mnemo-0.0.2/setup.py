# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mnemo', 'mnemo.bottled', 'mnemo.scripts', 'mnemo.tests']

package_data = \
{'': ['*'],
 'mnemo': ['autocomplete/*'],
 'mnemo.bottled': ['css/*',
                   'db/.gitignore',
                   'js/*',
                   'templates/*',
                   'templates/buttons/*',
                   'templates/forms/*',
                   'templates/includes/*',
                   'templates/pages/*',
                   'templates/responses/*']}

install_requires = \
['bottle>=0.12.19,<0.13.0',
 'click>=8.0.1,<9.0.0',
 'passlib>=1.7.4,<2.0.0',
 'paste>=3.5.0,<4.0.0',
 'rich>=10.4.0,<11.0.0',
 'tinydb>=4.5.0,<5.0.0']

entry_points = \
{'console_scripts': ['mnemo = mnemo.scripts.assistant:__main',
                     'mnemo-autocomplete = mnemo.scripts.autocomplete:__main']}

setup_kwargs = {
    'name': 'mnemo',
    'version': '0.0.2',
    'description': 'Notebook and assistant.',
    'long_description': "# mnemo-assistant\n\n![Release ID](https://img.shields.io/github/release/ggirelli/mnemo-assistant.svg?style=flat) ![Release date](https://img.shields.io/github/release-date/ggirelli/mnemo-assistant.svg?style=flat)  \n![PyPI - Python Version](https://img.shields.io/pypi/pyversions/mnemo) ![PyPI - Status](https://img.shields.io/pypi/status/mnemo) ![GitHub Actions Python package status](https://github.com/ggirelli/mnemo-assistant/workflows/Python%20package/badge.svg?branch=main&event=push)  \n![license](https://img.shields.io/github/license/ggirelli/mnemo-assistant.svg?style=flat) ![Code size](https://img.shields.io/github/languages/code-size/ggirelli/mnemo-assistant.svg?style=flat)  \n![Watch no.](https://img.shields.io/github/watchers/ggirelli/mnemo-assistant.svg?label=Watch&style=social) ![Stars no.](https://img.shields.io/github/stars/ggirelli/mnemo-assistant.svg?style=social)\n\n[PyPi](https://pypi.org/project/mnemo/) | [docs](https://ggirelli.github.io/mnemo-assistant/)\n\nA Python3.8+ web framework providing tools for journaling and note taking.\n\n## Features (in short)\n\n* Bottle-based web framework.\n* Login system (currently supports one user at a time).\n\n## Requirements\n\n`mnemo-assistant` has been tested with Python 3.8 and 3.9. We recommend installing it using `pipx` (see [below](https://github.com/ggirelli/mnemo-assistant#install)) to avoid dependency conflicts with other packages. The packages it depends on are listed in our [dependency graph](https://github.com/ggirelli/mnemo-assistant/network/dependencies). We use [`poetry`](https://github.com/python-poetry/poetry) to handle our dependencies.\n\n## Install\n\nWe recommend installing `mnemo-assistant` using [`pipx`](https://github.com/pipxproject/pipx). Check how to install `pipx` [here](https://github.com/pipxproject/pipx#install-pipx) if you don't have it yet! Once you have `pipx` ready on your system, install the latest stable release of `mnemo-assistant` by running: `pipx install mnemo-assistant`. If you see the stars (✨ 🌟 ✨), then the installation went well!\n\n## Usage\n\nRun `mnemo` to access the barber's services. Add `-h` to see the full help page of a command! Also, run `mnemo-autocomplete -s BASH_TYPE` to activate autocompletion. `BASH_TYPE` currently supports: `bash`, `fish`, and `zsh`.\n\n## Contributing\n\nWe welcome any contributions to `mnemo-assistant`. In short, we use [`black`](https://github.com/psf/black) to standardize code format. Any code change also needs to pass `mypy` checks. For more details, please refer to our [contribution guidelines](https://github.com/ggirelli/mnemo-assistant/blob/main/CONTRIBUTING.md) if this is your first time contributing! Also, check out our [code of conduct](https://github.com/ggirelli/mnemo-assistant/blob/main/CODE_OF_CONDUCT.md).\n\n## License\n\n`MIT License - Copyright (c) 2021 Gabriele Girelli`\n",
    'author': 'Gabriele Girelli',
    'author_email': 'gigi.ga90@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ggirelli/mnemo-assistant',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
