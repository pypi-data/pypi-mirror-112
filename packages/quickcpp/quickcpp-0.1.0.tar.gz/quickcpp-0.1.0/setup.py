# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['quickcpp']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['quickcpp = quickcpp.main:main']}

setup_kwargs = {
    'name': 'quickcpp',
    'version': '0.1.0',
    'description': 'Quickly builds a standalone C++ file and runs the result.',
    'long_description': None,
    'author': 'Aurelien Gateau',
    'author_email': 'mail@agateau.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.6.2,<4.0.0',
}


setup(**setup_kwargs)
