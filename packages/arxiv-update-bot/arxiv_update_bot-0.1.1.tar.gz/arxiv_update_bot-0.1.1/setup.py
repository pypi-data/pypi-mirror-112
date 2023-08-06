# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['arxiv_update_bot']

package_data = \
{'': ['*']}

install_requires = \
['feedparser>=6.0.8,<7.0.0', 'pyTelegramBotAPI>=3.8.1,<4.0.0']

entry_points = \
{'console_scripts': ['arxiv-update-bot = arxiv_update_bot.main:main']}

setup_kwargs = {
    'name': 'arxiv-update-bot',
    'version': '0.1.1',
    'description': 'A bot to monitor arXiv updates',
    'long_description': '# arXiv update bot\n\narxiv update bot is a simple python script that scraps the arXiv, search for interesting paper and send a message on telegram if any was found.\n\n## Usage\n\nThe package comes with a command line script arxiv-update-bot. Here the help message :\n\n```\nusage: arxiv-update-bot [-h] [-c CONFIG_PATH] [-q]\n\nScrap the arXiv\n\noptional arguments:\n  -h, --help            show this help message and exit\n  -c CONFIG_PATH, --config-path CONFIG_PATH\n                        Path for configuration path. Replace default of\n                        /etc/arxiv-update-bot/config.ini\n  -q, --quiet           If quiet is set, then the bot will not send message if\n                        no article are found.\n```\n\n## Installation\n\nThe package can be installed either via the pypi repository :\n\nor using the sources :\n\n## Configuration file\n\nIn order to work, the script needs a configuration file. It will by default search for the configuration file in `/etc/arxiv-update-bot/config.ini`. Note that you have to manually create the folder and give the good permissions.\n\nYou can override the default behavior with the `-c` option on the command line and by giving the path as argument.\n\nAn example configuration can be found at `arxiv_update_bot/config.example.ini` and is also included in the package. Here is the example:\n\n```ini\n[bot]\ntoken = 0000000000:AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA\n\n[quant-ph]\nchat_id = 0\ncategory = quant-ph\nbuzzwords = cvqkd,continuous variable,continuous-variable,qkd,quantum key distribution,rfsoc,fpga\n```\n\nThe `[bot]` section is here to parametrize the bot. It must have the `token` value (with the "bot" word).\n\nThen for each update, you need to define a section. The name of the section is not really important (it must be unique and not "bot"). \n* The `chat_id` corresponds to the id of the individual or group where the notification must be sent. For now you can only configure 1 recipient per update.\n* The `category` is the name of the arxiv category. It will be used to determinate which RSS flux will be scraped.\n* The `buzzwords` are a list of words, separated by comas (without spaces) and in lowercase. The articles that will be keeped will be the ones with one of the buzwwords in the title.\n\n## Cron configuration\n\nIt is advised to use a cron to execute the script periodically :\n\n\n## How it works\n\nFor each update, the script get the RSS flux, goes through the article and try to match the articles titles with the buzzwords. If there is match, a notification is sent.',
    'author': 'Yoann Piétri',
    'author_email': 'me@nanoy.fr',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/nanoy42/arxiv-update-bot',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
