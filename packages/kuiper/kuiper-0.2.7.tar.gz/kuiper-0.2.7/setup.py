# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['kuiper', 'kuiper.models', 'kuiper.tui']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML==5.3', 'sqlalchemy==1.4.20']

entry_points = \
{'console_scripts': ['kuiper = kuiper.main:main']}

setup_kwargs = {
    'name': 'kuiper',
    'version': '0.2.7',
    'description': 'A terminal-based dating application for UTD students',
    'long_description': '# Kuiper\n\nA terminal-based dating application for UTD students, built with the `curses` api\n\n## Usage\nTo install: `$ pip install kuiper`\n\nTo start the TUI: `$ kuiper`\n\nTo view the help menu: `$ kuiper -h`\n\n## Inspiration\n[UTD Bruh Moments IG Post](https://www.instagram.com/p/CRCJhEmpbI0/)\n\n[Original Reddit Post](https://www.reddit.com/r/utdallas/comments/od9roi/how_easy_is_it_to_find_men_above_the_age_of_23_at/)\n',
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
