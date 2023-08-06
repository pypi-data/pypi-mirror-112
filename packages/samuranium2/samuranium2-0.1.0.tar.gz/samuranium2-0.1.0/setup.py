# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['src', 'src.exceptions', 'src.utils']

package_data = \
{'': ['*']}

install_requires = \
['Flask>=2.0.1,<3.0.0',
 'coverage>=5.5,<6.0',
 'ddt>=1.4.2,<2.0.0',
 'pylint>=2.9.3,<3.0.0',
 'selenium>=3.141.0,<4.0.0',
 'webdriver-manager>=3.4.2,<4.0.0']

setup_kwargs = {
    'name': 'samuranium2',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Alexis Giovoglanian',
    'author_email': 'alexisgiovoglanian@infovalue.com.ar',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
