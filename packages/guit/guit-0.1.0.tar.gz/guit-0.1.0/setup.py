# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['guit']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0', 'parse>=1.19.0,<2.0.0', 'sh>=1.14.2,<2.0.0']

extras_require = \
{':python_version < "3.8"': ['importlib-metadata>=1.0,<2.0']}

entry_points = \
{'console_scripts': ['guit = guit.cli:main']}

setup_kwargs = {
    'name': 'guit',
    'version': '0.1.0',
    'description': 'A Python CLI to open a web page from a Git repository.',
    'long_description': "# guit\n\n[![Open in Visual Studio Code](https://open.vscode.dev/badges/open-in-vscode.svg)](https://open.vscode.dev/joaopalmeiro/guit)\n[![PyPI](https://img.shields.io/pypi/v/guit)](https://pypi.org/project/guit/)\n[![Release](https://github.com/joaopalmeiro/toppics/actions/workflows/release.yml/badge.svg)](https://github.com/joaopalmeiro/guit/actions/workflows/release.yml)\n[![security: bandit](https://img.shields.io/badge/security-bandit-yellow.svg)](https://github.com/PyCQA/bandit)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n\nA Python CLI to open a web page from a [Git](https://git-scm.com/) repository.\n\n## References\n\n- Carl-Fredrik Arvidson's [git-open](https://github.com/cfarvidson/git-open) CLI\n- Aaron O'Mullan's [giturlparse.py](https://github.com/FriendCode/giturlparse.py) package\n\n## Development\n\n- `poetry install`\n- `poetry shell`\n\n## Tech Stack\n\n- [Click](https://click.palletsprojects.com/) (for the interface)\n\n### Packaging and Development\n\n- [Poetry](https://python-poetry.org/)\n- [Mypy](http://mypy-lang.org/)\n- [isort](https://pycqa.github.io/isort/)\n- [Black](https://github.com/psf/black)\n- [Flake8](https://flake8.pycqa.org/)\n  - [flake8-bugbear](https://github.com/PyCQA/flake8-bugbear)\n  - [flake8-comprehensions](https://github.com/adamchainz/flake8-comprehensions)\n  - [pep8-naming](https://github.com/PyCQA/pep8-naming)\n  - [flake8-builtins](https://github.com/gforcada/flake8-builtins)\n- [Bandit](https://bandit.readthedocs.io/)\n\nThis CLI was created with [Cookiecutter](https://github.com/audreyr/cookiecutter) and the [`joaopalmeiro/cookiecutter-templates/python-cli`](https://github.com/joaopalmeiro/cookiecutter-templates) project template.\n\n## Notes\n\n- [Click 7 documentation](https://click.palletsprojects.com/en/7.x/)\n- Delete a Git tag ([source](https://gist.github.com/mobilemind/7883996)):\n  - `git tag -d v0.1.0` (local)\n  - `git push origin :refs/tags/v0.1.0` (remote)\n",
    'author': 'João Palmeiro',
    'author_email': 'joaommpalmeiro@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/joaopalmeiro/guit',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
