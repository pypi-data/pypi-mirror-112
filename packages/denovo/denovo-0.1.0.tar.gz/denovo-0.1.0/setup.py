# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['denovo', 'denovo.core', 'denovo.utilities']

package_data = \
{'': ['*']}

install_requires = \
['more-itertools>=8.8.0,<9.0.0']

setup_kwargs = {
    'name': 'denovo',
    'version': '0.1.0',
    'description': 'handy tools and classes for a new python package',
    'long_description': '',
    'author': 'Corey Rayburn Yung',
    'author_email': 'coreyrayburnyung@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/WithPrecedent/fiat',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
