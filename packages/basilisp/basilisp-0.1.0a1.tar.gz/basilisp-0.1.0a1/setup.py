# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['basilisp', 'basilisp.lang', 'basilisp.lang.compiler']

package_data = \
{'': ['*']}

install_requires = \
['astor>=0.8',
 'attrs',
 'immutables>=0.15,<0.16',
 'prompt-toolkit>=3.0.0,<3.1.0',
 'pyrsistent',
 'python-dateutil',
 'readerwriterlock>=1.0.8,<1.1.0']

entry_points = \
{'console_scripts': ['basilisp = basilisp.cli:invoke_cli'],
 'pytest11': ['basilisp_test_runner = basilisp.testrunner']}

setup_kwargs = {
    'name': 'basilisp',
    'version': '0.1.0a1',
    'description': 'A Clojure-like lisp written for Python',
    'long_description': '# 🐍 basilisp 🐍\n\nA Lisp dialect inspired by Clojure targeting Python 3.\n\n**Disclaimer:** _Basilisp is a project I created to learn about Python, Clojure,\nand hosted languages generally. It should not be used in a production setting._\n\n[![PyPI](https://img.shields.io/pypi/v/basilisp.svg?style=flat-square)](https://pypi.org/project/basilisp/) [![python](https://img.shields.io/pypi/pyversions/basilisp.svg?style=flat-square)](https://pypi.org/project/basilisp/) [![pyimpl](https://img.shields.io/pypi/implementation/basilisp.svg?style=flat-square)](https://pypi.org/project/basilisp/) [![readthedocs](https://img.shields.io/readthedocs/basilisp.svg?style=flat-square)](https://basilisp.readthedocs.io/) [![CircleCI](\thttps://img.shields.io/circleci/project/github/basilisp-lang/basilisp/master.svg?style=flat-square)](https://circleci.com/gh/basilisp-lang/basilisp) [![Coveralls github](https://img.shields.io/coveralls/github/basilisp-lang/basilisp.svg?style=flat-square)](https://coveralls.io/github/basilisp-lang/basilisp) [![license](https://img.shields.io/github/license/basilisp-lang/basilisp.svg?style=flat-square)](https://github.com/basilisp-lang/basilisp/blob/master/LICENSE)\n\n## Getting Started\n\nBasilisp is developed on [GitHub](https://github.com/chrisrink10/basilisp)\nand hosted on [PyPI](https://pypi.python.org/pypi/basilisp). You can\nfetch Basilisp using a simple:\n\n```bash\npip install basilisp\n```\n\nOnce Basilisp is installed, you can enter into the REPL using:\n\n```bash\nbasilisp repl\n```\n\nBasilisp [documentation](https://basilisp.readthedocs.io) can help guide your \nexploration at the REPL. Additionally, Basilisp features many of the same functions \nand idioms as [Clojure](https://clojure.org/) so you may find guides and \ndocumentation there helpful for getting started.\n\n## Developing on Basilisp\n\n### Requirements\n\nThis project uses [`poetry`](https://github.com/python-poetry/poetry) to manage\nthe Python virtual environment, project dependencies, and package publication.\nSee the instructions on that repository to install in your local environment.\nBecause `basilisp` is intended to be used as a library, no `poetry.lock` file\nis committed to the repository. Developers should generate their own lock file\nand update it regularly during development instead.\n\nAdditionally, [`pyenv`](https://github.com/pyenv/pyenv) is recommended to \nmanage versions of Python readily on your local development environment.\nSetup of `pyenv` is somewhat more specific to your environment, so see\nthe documentation in the repository for more information.\n\n### Getting Started\n\nTo prepare your `poetry` environment, you need to install dependencies:\n\n```bash\npoetry install\n```\n\nAfterwards, you can start up the REPL for development with a simple:\n\n```bash\nmake repl\n```\n\n### Linting, Running Tests, and Type Checking\n\nBasilisp automates linting, running tests, and type checking using \n[Tox](https://github.com/tox-dev/tox). All three steps can be performed\nusing a simple `make` target:\n\n```bash\nmake test\n```\n\nTesting is performed using [PyTest](https://github.com/pytest-dev/pytest/). \nType checking is performed by [MyPy](http://mypy-lang.org/). Linting is \nperformed using [Prospector](https://prospector.landscape.io/en/master/).\n\n## License\n\nEclipse Public License 1.0\n',
    'author': 'Christopher Rink',
    'author_email': 'chrisrink10@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/basilisp-lang/basilisp',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
