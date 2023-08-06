# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['kuiper', 'kuiper.models']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML==5.3', 'sqlalchemy==1.4.20']

entry_points = \
{'console_scripts': ['kuiper = kuiper.main:main']}

setup_kwargs = {
    'name': 'kuiper',
    'version': '0.1.0',
    'description': 'A terminal-based dating application for UTD students',
    'long_description': None,
    'author': 'CharlesAverill',
    'author_email': 'charlesaverill20@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
