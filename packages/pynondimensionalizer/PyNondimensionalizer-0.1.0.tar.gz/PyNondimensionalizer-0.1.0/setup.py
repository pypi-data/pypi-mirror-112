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
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Doug Keller',
    'author_email': 'dg.kllr.jr@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
