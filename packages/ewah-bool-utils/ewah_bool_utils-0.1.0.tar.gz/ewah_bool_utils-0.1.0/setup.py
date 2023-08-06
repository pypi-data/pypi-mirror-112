# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ewah_bool_utils']

package_data = \
{'': ['*'], 'ewah_bool_utils': ['cpp/*']}

install_requires = \
['Cython>=0.29.21,<3.0', 'flake8>=3.9.2,<4.0.0', 'numpy']

setup_kwargs = {
    'name': 'ewah-bool-utils',
    'version': '0.1.0',
    'description': 'EWAH Bool Array utils for yt',
    'long_description': None,
    'author': 'Matthew Turk',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
