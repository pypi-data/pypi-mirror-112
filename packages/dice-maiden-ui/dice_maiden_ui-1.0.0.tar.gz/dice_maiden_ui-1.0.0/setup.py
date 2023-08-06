# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dice_maiden_ui']

package_data = \
{'': ['*']}

install_requires = \
['jsonschema>=3.2.0,<4.0.0', 'pyperclip>=1.8.2,<2.0.0']

entry_points = \
{'console_scripts': ['dice_maiden_ui = dice_maiden_ui.__main__:run']}

setup_kwargs = {
    'name': 'dice-maiden-ui',
    'version': '1.0.0',
    'description': 'GUI application designed to generate dice maiden roll commands',
    'long_description': "[![CircleCI](https://circleci.com/gh/jjmar/dice-maiden-ui/tree/main.svg?style=svg)](https://circleci.com/gh/jjmar/dice-maiden-ui/tree/main)\n\n\n# dice-maiden-ui\nPython app which helps to generate roll commands for the [dice maiden discord app](https://top.gg/bot/377701707943116800).\n\nYou create a configuration file listing the details of your commands. When running the app, you select your configuration file\nwhich will generate the UI.\n\nBefore selecting the command you'd like to roll, select any options for the roll.\nThen upon clicking a command button, the generated roll will be automatically copied to your clipboard.\n\n![Dice Maiden UI](documentation/gui.png)\n\n\n# Installing the app\n\n`pip install dice-maiden-ui`\n\n\n# Running the app\n\n1) Ensure you've created your configuration file - see the [configuration setup doc](documentation/config.md).\n2) Run the app with either `dice_maiden_ui` or `python -m dice_maiden_ui`\n3) In the top left, click `Open` and find your configuration file from step 1\n\n",
    'author': 'Justin Martin',
    'author_email': 'jjmardev@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/jjmar/dice-maiden-ui',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
