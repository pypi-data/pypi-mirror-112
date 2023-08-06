# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['appman',
 'appman.buckets',
 'appman.buckets.main',
 'appman.buckets.main.formulas',
 'appman.buckets.main.packages',
 'appman.buckets.main.packages.apps',
 'appman.buckets.main.packages.backend',
 'appman.buckets.main.packages.backend.node',
 'appman.buckets.main.packages.backend.python',
 'appman.buckets.main.packages.drivers',
 'appman.buckets.main.packages.extensions',
 'appman.buckets.main.packages.extensions.vscode',
 'appman.buckets.main.packages.fonts',
 'appman.buckets.main.packages.provisioned',
 'appman.logs',
 'appman.user',
 'appman.user.data']

package_data = \
{'': ['*']}

install_requires = \
['PyInquirer>=1.0.3,<2.0.0',
 'click>=8.0.1,<9.0.0',
 'distro>=1.5.0,<2.0.0',
 'importlib-resources>=5.2.0,<6.0.0',
 'pyyaml>=5.3.1,<6.0.0']

entry_points = \
{'console_scripts': ['appman = appman.cli:main']}

setup_kwargs = {
    'name': 'appman',
    'version': '0.4.0',
    'description': 'Cross-platform application management aggregator',
    'long_description': '# appman\n\nappman is cross-platform application management aggregator\n\n[![Build Status](https://travis-ci.com/basiliskus/appman.svg?branch=main)](https://travis-ci.com/basiliskus/appman)\n\n<p align="center"><img src="https://raw.githubusercontent.com/basiliskus/appman/main/docs/demo.gif"/></p>\n\n## Requirements\n\n- Python 3.8\n\n## Installation\n\nYou can install appman from [PyPI](https://pypi.org/project/appman/):\n\n```bash\n> pip install appman\n```\n\n## Background\n\nWhile working on my [dotfiles](https://wiki.archlinux.org/title/Dotfiles) repository, I realized that I also wanted to have a way to handle not just configuration files but also my installed applications. That way I\'d be able to define which applications I want to have installed on any new environment, have those under version control, and run a script to install/uninstall applications on any new personal or work computer, server, etc.\n\n## Goals\n\nThe main goal for appman is to be flexible and extensible. In that context the goals are:\n\n- Cross-platform: handle multiple OS and devices. Currently appman handles Ubuntu and Windows (desktop).\n- Multi-profile: define different profiles with a unique list of applications for different environments (e.g., work and personal computers).\n- Supported Packages: aside from desktop and command line applications, support software like: device drivers, software plugins and extensions (e.g., vscode extensions), backend libraries (e.g., python libraries), fonts, etc.\n- Package Management: support any package manager (e.g., apt, brew, scoop) or custom formulas to define how to install, uninstall and upgrade packages.\n- Buckets: currently there is only [one source](https://github.com/basiliskus/appman/tree/main/appman/buckets/main) to choose packages from, but the idea is to have any user able to create their own buckets which can then be shared and used by other users.\n\n## How to use\n\n### Set up your user package list\n\n- Add a package to your user packages list\n\n  Using interactive mode:\n\n  ```console\n  $ appman add\n\n  [?] Select the package type: (Use arrow keys)\n  >app\n   font\n   driver\n   provisioned\n   backend\n   extension\n\n  [?] Select app packages to add: (<up>, <down> to move, <space> to select, <a> to toggle, <i> to invert)\n   ○ curl\n   ○ fzf\n  >● git\n   ○ jq\n   ○ python\n   ○ ...\n\n  Added git package\n  ```\n\n  or directly passing parameters:\n\n  ```console\n  $ appman add -pt app -id git\n  ```\n\n- Remove a previously added package\n\n  Using interactive mode:\n\n  ```console\n  $ appman remove\n\n  [?] Select the package type: (Use arrow keys)\n  >app\n   font\n   driver\n   provisioned\n   backend\n   extension\n\n  [?] Select app packages to remove: (<up>, <down> to move, <space> to select, <a> to toggle, <i> to invert)\n   ○ 7zip\n   ○ curl\n  >● git\n   ○ ...\n\n  Removed git package\n  ```\n\n  Directly passing parameters:\n\n  ```console\n  $ appman remove -pt app -id git\n  ```\n\n- Show your user packages list\n\n  Using interactive mode:\n\n  ```console\n  $ appman list\n\n  [?] Select the package type: (Use arrow keys)\n  >app\n\n   • 7zip (cli, utils)\n   • curl (cli, utils)\n  ```\n\n  Directly passing parameters:\n\n  ```console\n  $ appman list -pt app\n  ```\n\n- Search all available packages to add\n\n  Using interactive mode:\n\n  ```console\n  $ appman search\n\n  [?] Select the package type: (Use arrow keys)\n  >app\n\n  7zip\n  ack\n  apache2\n  aria2\n  bottom\n  broot\n  cookiecutter\n  curl\n  ...\n  ```\n\n  Directly passing parameters:\n\n  ```console\n  $ appman search -pt app -id 7zip\n  ```\n\n### Install/Uninstall packages in your user packages list\n\nUsing interactive mode:\n\n```console\n$ appman install\n\n[?] Select the package type: (Use arrow keys)\n>app\n\nInstalling 7zip...\nInstalling ack...\n...\n```\n\nDirectly passing parameters:\n\n```console\n$ appman install -pt app -id 7zip\n```\n\n### Using labels\n\nAll packages have pre-defined labels (e.g. for apps: \'cli\' & \'gui\'), but you can also add your own labels by passing the --labels/-l parameter to the \'add\' command.\n\n```console\n$ appman add -pt app -id 7zip -l server\n```\n\nYou can also filter by labels when using the \'list\', \'search\', \'remove\', \'install\' or \'uninstall\' commands\n\n```console\n$ appman list -pt app -l server\n```\n\n## License\n\n© Basilio Bogado. Distributed under the [MIT License](LICENSE).\n',
    'author': 'Basilio Bogado',
    'author_email': '541149+basiliskus@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/basiliskus/appman',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
