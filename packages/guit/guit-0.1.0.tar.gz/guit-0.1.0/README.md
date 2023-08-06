# guit

[![Open in Visual Studio Code](https://open.vscode.dev/badges/open-in-vscode.svg)](https://open.vscode.dev/joaopalmeiro/guit)
[![PyPI](https://img.shields.io/pypi/v/guit)](https://pypi.org/project/guit/)
[![Release](https://github.com/joaopalmeiro/toppics/actions/workflows/release.yml/badge.svg)](https://github.com/joaopalmeiro/guit/actions/workflows/release.yml)
[![security: bandit](https://img.shields.io/badge/security-bandit-yellow.svg)](https://github.com/PyCQA/bandit)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

A Python CLI to open a web page from a [Git](https://git-scm.com/) repository.

## References

- Carl-Fredrik Arvidson's [git-open](https://github.com/cfarvidson/git-open) CLI
- Aaron O'Mullan's [giturlparse.py](https://github.com/FriendCode/giturlparse.py) package

## Development

- `poetry install`
- `poetry shell`

## Tech Stack

- [Click](https://click.palletsprojects.com/) (for the interface)

### Packaging and Development

- [Poetry](https://python-poetry.org/)
- [Mypy](http://mypy-lang.org/)
- [isort](https://pycqa.github.io/isort/)
- [Black](https://github.com/psf/black)
- [Flake8](https://flake8.pycqa.org/)
  - [flake8-bugbear](https://github.com/PyCQA/flake8-bugbear)
  - [flake8-comprehensions](https://github.com/adamchainz/flake8-comprehensions)
  - [pep8-naming](https://github.com/PyCQA/pep8-naming)
  - [flake8-builtins](https://github.com/gforcada/flake8-builtins)
- [Bandit](https://bandit.readthedocs.io/)

This CLI was created with [Cookiecutter](https://github.com/audreyr/cookiecutter) and the [`joaopalmeiro/cookiecutter-templates/python-cli`](https://github.com/joaopalmeiro/cookiecutter-templates) project template.

## Notes

- [Click 7 documentation](https://click.palletsprojects.com/en/7.x/)
- Delete a Git tag ([source](https://gist.github.com/mobilemind/7883996)):
  - `git tag -d v0.1.0` (local)
  - `git push origin :refs/tags/v0.1.0` (remote)
