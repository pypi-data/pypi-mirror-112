# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['groklog',
 'groklog.filter_manager',
 'groklog.process_node',
 'groklog.ui',
 'groklog.ui.scenes']

package_data = \
{'': ['*']}

install_requires = \
['asciimatics>=1.13.0,<2.0.0',
 'pre-commit>=2.13.0,<3.0.0',
 'pubsus>=0.1.1,<0.2.0']

entry_points = \
{'console_scripts': ['groklog = groklog:main']}

setup_kwargs = {
    'name': 'groklog',
    'version': '0.1.0',
    'description': 'A tool for filtering logs quickly and easily',
    'long_description': None,
    'author': 'Alex Thiel',
    'author_email': 'apocthiel@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
