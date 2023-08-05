# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyfurc']

package_data = \
{'': ['*']}

install_requires = \
['appdirs', 'numpy', 'pandas', 'pydata-sphinx-theme', 'sphinx', 'sympy']

setup_kwargs = {
    'name': 'pyfurc',
    'version': '0.1.7',
    'description': 'AUTO-07p made accessible through python.',
    'long_description': None,
    'author': 'klunkean',
    'author_email': 'klunkean@posteo.de',
    'maintainer': 'klunkean',
    'maintainer_email': 'klunkean@posteo.de',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
