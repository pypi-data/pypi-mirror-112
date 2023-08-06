# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pynondimensionalizer']

package_data = \
{'': ['*']}

install_requires = \
['argparse>=1.4.0,<2.0.0',
 'pandas>=1.2.1,<2.0.0',
 'pathlib>=1.0.1,<2.0.0',
 'sympy>=1.7.1,<2.0.0']

setup_kwargs = {
    'name': 'pynondimensionalizer',
    'version': '0.1.2',
    'description': 'A command line program that calculates the nullspace vector from a given dimensional matrix.',
    'long_description': "# PyNondimensionalizer\n\nA simple little command line program in python to help find nondimensional numbers, such as the Reynold's number, Rossby number, or more.\n\nSee the [documentation](https://alaskanresearcher.dev/pynondimensionalizer/pynondimensionalizer.html) for more information.\n",
    'author': 'Doug Keller',
    'author_email': 'dg.kllr.jr@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/dkllrjr/PyNondimensionalizer',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
