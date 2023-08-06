# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyrepositoryminer',
 'pyrepositoryminer.commands',
 'pyrepositoryminer.metrics',
 'pyrepositoryminer.metrics.diffdir',
 'pyrepositoryminer.metrics.dir',
 'pyrepositoryminer.metrics.nativeblob',
 'pyrepositoryminer.metrics.nativetree']

package_data = \
{'': ['*']}

install_requires = \
['pygit2>=1.5.0,<2.0.0',
 'radon>=4.5.0,<5.0.0',
 'typer[all]>=0.3.2,<0.4.0',
 'uvloop>=0.15.2,<0.16.0']

entry_points = \
{'console_scripts': ['pyrepositoryminer = pyrepositoryminer:app']}

setup_kwargs = {
    'name': 'pyrepositoryminer',
    'version': '0.7.0',
    'description': 'Efficient Repository Mining in Python',
    'long_description': '# pyrepositoryminer\n\n[![CI workflow](https://github.com/fabianhe/pyrepositoryminer/actions/workflows/test.yaml/badge.svg)](https://github.com/fabianhe/pyrepositoryminer/actions/workflows/test.yaml)\n[![PyPI Python version](https://img.shields.io/pypi/pyversions/pyrepositoryminer?color=000000)](https://pypi.org/project/pyrepositoryminer/)\n[![PyPI package](https://img.shields.io/pypi/v/pyrepositoryminer?color=%23000)](https://pypi.org/project/pyrepositoryminer/)\n[![Tokei](https://tokei.rs/b1/github/fabianhe/pyrepositoryminer)](https://tokei.rs)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n[![PyPI downloads](https://img.shields.io/pypi/dm/pyrepositoryminer?color=000000)](https://pypi.org/project/pyrepositoryminer/)\n\nThe pyrepositoryminer aims to be a **performant**, **extendable** and **useful** tool for analyzing (large) software repositories.\n\n## Installation\n\nInstall it from [PyPI](https://pypi.org/project/pyrepositoryminer/):\n\n```console\n$ pip install pyrepositoryminer\n```\n\n### Requirements\n\n**Python 3.9+**, libgit2 (e.g. `brew install libgit2` on macOS).\n\npyrepositoryminer builds on the work of [pygit2](https://github.com/libgit2/pygit2) for the interaction with git repository objects, [typer](https://github.com/tiangolo/typer) for the CLI, [radon](https://github.com/rubik/radon) for Python-specific metrics, and [uvloop](https://github.com/MagicStack/uvloop) for an alternative event loop.\n\n## Contributing\n\nInstall [poetry](https://github.com/python-poetry/poetry):\n\n```console\n$ curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py | python -\n```\n\nInstall the dependencies:\n\n```console\n$ poetry install\n```\n\nInstall the [pre-commit](https://github.com/pre-commit/pre-commit) hooks:\n\n```console\n$ pre-commit install\n```\n',
    'author': 'Fabian Heseding',
    'author_email': '39628987+fabianhe@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/fabianhe/pyrepositoryminer',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
