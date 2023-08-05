# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['beancount_rabobank']

package_data = \
{'': ['*'], 'beancount_rabobank': ['test_files/*']}

setup_kwargs = {
    'name': 'beancount-rabobank',
    'version': '0.1.0',
    'description': 'Beancount importer for Rabobank CSV exports',
    'long_description': None,
    'author': 'Marijn van Aerle',
    'author_email': 'marijn.vanaerle@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/mvaerle/beancount-rabobank',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
