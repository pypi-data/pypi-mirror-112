# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['dessinemoi']

package_data = \
{'': ['*']}

install_requires = \
['attrs']

setup_kwargs = {
    'name': 'dessinemoi',
    'version': '21.2.0',
    'description': 'A simple Python factory system',
    'long_description': "# Dessine-moi, a simple Python factory\n\n> S'il vous plaît, dessine-moi un mouton.\n\nThe narrator of Antoine de Saint-Exupéry's Little Prince probably dreamt of a factory like this one...\n\n[![PyPI version](https://img.shields.io/pypi/v/dessinemoi?color=blue&style=flat-square)](https://pypi.org/project/dessinemoi)\n[![Conda version](https://img.shields.io/conda/v/eradiate/dessinemoi?color=blue&style=flat-square)](https://anaconda.org/eradiate/dessinemoi)\n\n[![GitHub Workflow Status (branch)](https://img.shields.io/github/workflow/status/leroyvn/dessinemoi/Tests/main?style=flat-square)](https://github.com/leroyvn/dessinemoi/actions/workflows/tests.yml)\n[![Codecov](https://codecov.io/gh/leroyvn/dessinemoi/branch/main/graph/badge.svg)](https://codecov.io/gh/leroyvn/dessinemoi)\n[![Documentation Status](https://img.shields.io/readthedocs/dessinemoi?style=flat-square)](https://dessinemoi.readthedocs.io)\n\n[![Code style: black](https://img.shields.io/badge/code%20style-black-black?style=flat-square)](https://black.readthedocs.io)\n[![Imports: isort](https://img.shields.io/badge/%20imports-isort-blue?style=flat-square&labelColor=orange)](https://pycqa.github.io/isort)\n\n## Motivation\n\n*Dessine-moi* is a simple Python implementation of the factory pattern. It was \nborn from the need to create dynamically object trees from nested dictionaries \n(*e.g.* a JSON document).\n\n## Features\n\n- Create a `Factory` object and register types to it\n- Use dictionaries to create objects from the factory\n- Create `attrs`-compatible converters to automatically convert dictionaries to \n  instances of registered types\n- Customise factories to your needs\n\nCheck the [documentation](https://dessinemoi.readthedocs.io) for more detail.\n\n## License\n\n*Dessine-moi* is distributed under the terms of the\n[MIT license](https://choosealicense.com/licenses/mit/).\n\n## About\n\n*Dessine-moi* is written and maintained by [Vincent Leroy](https://github.com/leroyvn).\n\nThe development is supported by [Rayference](https://www.rayference.eu).\n\n*Dessine-moi* is a component of the\n[Eradiate radiative transfer model](https://www.eradiate.eu).\n",
    'author': 'Vincent Leroy',
    'author_email': 'vincent.leroy@rayference.eu',
    'maintainer': 'Vincent Leroy',
    'maintainer_email': 'vincent.leroy@rayference.eu',
    'url': 'https://github.com/leroyvn/dessinemoi',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4',
}


setup(**setup_kwargs)
