# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rfd']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4<4.9.4',
 'click>=7.0',
 'colorama>=0.4.3',
 'requests>=2.22.0',
 'soupsieve<3.0']

entry_points = \
{'console_scripts': ['rfd = rfd.__main__:cli']}

setup_kwargs = {
    'name': 'rfd',
    'version': '0.7.2',
    'description': 'view RedFlagDeals.com from the command line',
    'long_description': '# RFD\n\n[![PyPI version](https://badge.fury.io/py/rfd.svg)](https://badge.fury.io/py/rfd)\n[![Dependabot](https://badgen.net/badge/Dependabot/enabled/green?icon=dependabot)](https://dependabot.com/)\n[![Downloads](https://pepy.tech/badge/rfd)](https://pepy.tech/project/rfd)\n\n<!-- BEGIN mktoc -->\n- [Description](#description)\n- [Motivation](#motivation)\n- [Installation](#installation)\n- [Usage](#usage)\n  - [View Hot Deals](#view-hot-deals)\n  - [View and Sort Hot Deals](#view-and-sort-hot-deals)\n  - [Search](#search)\n    - [Advanced](#advanced)\n  - [View Posts](#view-posts)\n- [Shell Completion](#shell-completion)\n  - [bash](#bash)\n  - [zsh](#zsh)\n<!-- END mktoc -->\n\n## Description\n\nThis is a CLI utility that allows you to view [RedFlagDeals.com](https://forums.redflagdeals.com) on the command line.\n\n![screenshot](https://user-images.githubusercontent.com/4519234/85969861-e10a4100-b996-11ea-9a31-6203322c60ee.png)\n\n## Motivation\n\nIt is often faster to use a CLI than to load up a web page and navigate web elements. This tool can search for deals and sort them based on score and views. It is also able to load entire threads (without pagination) for additional analysis.\n\n## Installation\n\n> :information_source: python2 may still work but it is [no longer supported](https://www.python.org/doc/sunset-python-2/).\n\n```bash\npython3 -m pip install --user rfd\n```\n\nAfter installation, if you cannot access `rfd` in your path, try `python3 -m rfd`.\n\n\n## Usage\n\nAll commands open up in a [terminal pager](https://en.wikipedia.org/wiki/Terminal_pager).\n\n```sh\nUsage: rfd [OPTIONS] COMMAND [ARGS]...\n\n  CLI for https://forums.redflagdeals.com\n\nOptions:\n  -v, --version\n  --help         Show this message and exit.\n\nCommands:\n  posts    Display all posts in a thread.\n  search   Search deals based on a regular expression.\n  threads  Displays threads in the forum. Defaults to hot deals.\n```\n\n### View Hot Deals\n\nTo view the threads on most popular sub-forum:\n\n```sh\nrfd threads\n```\n\n### View and Sort Hot Deals\n\n```sh\nrfd threads --sort-by score\n```\n\nTo view and sort multiple pages, use `--pages`:\n\n```sh\nrfd threads --sort-by views --pages 10\n```\n\n### Search\n\n```sh\nrfd search \'pizza\'\n```\n\n#### Advanced\n\nRegular expressions can be used for search.\n\n```sh\nrfd search \'(coffee|starbucks)\' --pages 10 --sort-by views\n```\n\n### View Posts\n\nIt\'s possible to view an entire post and all comments by running:\n\n```sh\nrfd posts https://forums.redflagdeals.com/kobo-vs-kindle-2396227/\n```\n\nThis allows for easy grepping and searching for desired expressions.\n\n## Shell Completion\n\nShell completion can be enabled if using `bash` or `zsh`.\n\n### bash\n\n```sh\necho \'eval "$(_RFD_COMPLETE=source rfd)"\' >> ~/.profile\n```\n\n### zsh\n\n```sh\necho \'eval "$(_RFD_COMPLETE=source_zsh rfd)"\' >> ~/.zshrc\n```\n',
    'author': 'Dave Gallant',
    'author_email': 'davegallant@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
