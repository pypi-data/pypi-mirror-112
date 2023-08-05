# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sofascore']

package_data = \
{'': ['*']}

install_requires = \
['pandas>=1.3.0,<2.0.0', 'tables>=3.6.1,<4.0.0']

setup_kwargs = {
    'name': 'sofascore',
    'version': '1.1.0',
    'description': '',
    'long_description': None,
    'author': 'shimst3r',
    'author_email': 'shimst3r@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
