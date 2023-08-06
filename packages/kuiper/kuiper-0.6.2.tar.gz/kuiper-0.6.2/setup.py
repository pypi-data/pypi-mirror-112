# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['kuiper', 'kuiper.models', 'kuiper.remote', 'kuiper.tui']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML==5.3',
 'sqlalchemy==1.4.20',
 'update-checker==0.18.0',
 'websockets==9.1']

entry_points = \
{'console_scripts': ['kuiper = kuiper.main:main']}

setup_kwargs = {
    'name': 'kuiper',
    'version': '0.6.2',
    'description': 'A terminal-based dating application for UTD students',
    'long_description': '# Kuiper\n\nA terminal-based dating application for UTD students, built with the `curses` API.\n\n## Installation\n\nUnfamiliar with terminal stuff? Here\'s what you need to start using Kuiper:\n\n1. [Install Python](https://www.python.org/downloads/release/python-379/)\n2. Open up your terminal or command line\n3. Type in `python3 -m pip install kuiper`. You may receive some nasty output, that\'s alright. Mac users might need to install XCode tools\n4. Now you\'re ready to use Kuiper! Just type `kuiper` into your command line, and the TUI should boot.\n\n## Usage\n```bash\n$ kuiper                       # Start the TUI\n$ kuiper -c USERNAME PASSWORD  # Login with credentials\n$ kuiper -d                    # Print configs\n$ kuiper -i                    # Initialize the database\n$ kuiper -h                    # View the help menu\n$ kuiper -l new_configs.yaml   # Update server configs\n$ kuiper --local_server        # Connect to localhost server\n$ kuiper -q                    # Suppress server output\n$ kuiper -s                    # Start server\n```\n\nMenu navigation is controlled by the up and down arrow keys.\n\nWhen filling out a form field, the string in the bottom-right corner is the current buffer. \nHit "Enter" to save the form field.\n\n## Configs\n\nThe follow are the configuration options supported by Kuiper. \n\nTo modify Kuiper\'s configs, create a `config.yaml` file with the keys and values you\'d like to overwrite, \nand call `kuiper -l config.yaml`\n\n| Config | Default Value | Description |\n| --- | --- | --- |\n| bind_host | "127.0.0.1" | The address on which the server will be hosted via `kuiper -s` |\n| port | 8000 | The port on which the server will be hosted via `kuiper -s`\n| access_host | "35.172.42.184" | The address to the server the client will ping. The defualt value is the static IP address of Kuiper\'s main server |\n| db_path | "kuiper.db" | The path to the server\'s user and post database |\n| required_email_suffix | "@utdallas.edu" | The email suffix required during registration. For no requirement, set to `""` |\n| text_editor | "vim" | The text editor called via the `subprocess` module to write posts and comments |\n\n\n## Inspiration\n[UTD Bruh Moments IG Post](https://www.instagram.com/p/CRCJhEmpbI0/)\n\n[Original Reddit Post](https://www.reddit.com/r/utdallas/comments/od9roi/how_easy_is_it_to_find_men_above_the_age_of_23_at/)\n',
    'author': 'CharlesAverill',
    'author_email': 'charlesaverill20@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/CharlesAverill/kuiper',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
