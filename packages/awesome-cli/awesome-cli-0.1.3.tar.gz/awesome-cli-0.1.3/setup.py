# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['awesome_cli', 'awesome_cli.commands']

package_data = \
{'': ['*'], 'awesome_cli': ['data/*']}

install_requires = \
['cleo>=0.8.1,<0.9.0',
 'colorful>=0.5.4,<0.6.0',
 'lxml>=4.6.3,<5.0.0',
 'mistune>=0.8.4,<0.9.0']

entry_points = \
{'console_scripts': ['awesome-cli = awesome_cli:main']}

setup_kwargs = {
    'name': 'awesome-cli',
    'version': '0.1.3',
    'description': 'Awesome CLI search',
    'long_description': "Awesome CLI\n===========\n\nAwesome List in CLI search (WIP)\n\n\n✨✨✨ *So Awesome* ✨✨✨\n\n\nCurrent *Awesome* Support:\n\n* [agarrharr/awesome-cli-apps](https://github.com/agarrharr/awesome-cli-apps)\n\n\nQuick Start\n-----------\n\nShow all awesome list\n\n```\n$ awesome-cli\n✨ Entertainment\nfootball-cli - Get live scores, fixtures, standings of almost every football competition/league.\n🔗 https://github.com/ManrajGrover/football-cli\npockyt - Read, Manage, and Automate your Pocket collection.\n🔗 https://github.com/arvindch/pockyt\nnewsboat - An extendable RSS feed reader for text terminals.\n🔗 https://github.com/newsboat/newsboat\n\n- 💥 Music\ncmus - Small, fast and powerful console music player.\n...\n```\n\nShow header only\n\n```\n$ awesome-cli -k\n✨ Entertainment\n- 💥 Music\n- 💥 Social Media\n- 💥 Video\n- 💥 Movies\n- 💥 Games\n- 💥 Books\n✨ Development\n- 💥 Text Editors\n...\n```\n\nDon't show URL\n\n```\n$ awesome-cli -u\n✨ Entertainment\nfootball-cli - Get live scores, fixtures, standings of almost every football competition/league.\npockyt - Read, Manage, and Automate your Pocket collection.\nnewsboat - An extendable RSS feed reader for text terminals.\n\n- 💥 Music\ncmus - Small, fast and powerful console music player.\n...\n```\n\nInstall\n-------\n\n```\n$ python -m pip install awesome-cli\n```\n\n\nPrerequirements\n---------------\n\n* poetry\n\nBuild\n-----\n\n```\n$ poetry build\n```\n\nTODO\n----\n\n- [ ] Support multi awesome list\n- [ ] Support search\n- [ ] Support showing specific section only\n",
    'author': 'Louie Lu',
    'author_email': 'git@louie.lu',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/mlouielu/awesome-cli',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
