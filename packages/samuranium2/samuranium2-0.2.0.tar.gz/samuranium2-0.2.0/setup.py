# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['Samuranium', 'Samuranium.exceptions', 'Samuranium.utils']

package_data = \
{'': ['*']}

install_requires = \
['selenium>=3.141.0,<4.0.0', 'webdriver-manager>=3.4.2,<4.0.0']

setup_kwargs = {
    'name': 'samuranium2',
    'version': '0.2.0',
    'description': 'Samuranium Automation Framework',
    'long_description': None,
    'author': 'Alexis Giovoglanian (malazay)',
    'author_email': 'alexisgiovoglanian@southerncode.us',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
