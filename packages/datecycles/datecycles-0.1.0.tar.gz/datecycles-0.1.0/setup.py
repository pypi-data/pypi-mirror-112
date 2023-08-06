# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['datecycles']

package_data = \
{'': ['*']}

install_requires = \
['arrow>=1.1.1,<2.0.0', 'holidays>=0.11.1,<0.12.0']

setup_kwargs = {
    'name': 'datecycles',
    'version': '0.1.0',
    'description': 'Simple library for complicated date cycling rules',
    'long_description': None,
    'author': 'Niko Järvinen',
    'author_email': 'nbjarvinen@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
