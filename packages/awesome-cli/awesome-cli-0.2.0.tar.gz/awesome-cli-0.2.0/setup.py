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
 'mistune>=0.8.4,<0.9.0',
 'prompt-toolkit>=3.0.19,<4.0.0']

entry_points = \
{'console_scripts': ['awesome-cli = awesome_cli:main']}

setup_kwargs = {
    'name': 'awesome-cli',
    'version': '0.2.0',
    'description': 'Awesome CLI search',
    'long_description': "Awesome CLI\n===========\n\nAwesome List in CLI search (WIP)\n\n\n✨✨✨ *So Awesome* ✨✨✨\n\n\nCurrent *Awesome* Support:\n\n* [agarrharr/awesome-cli-apps](https://github.com/agarrharr/awesome-cli-apps)\n\n\nQuick Start\n-----------\n\nInteractive query\n\n```\n$ awesome-cli -i\nPlease select one section to show: 18.  - Time Tracking (5) [RET]\n                00.  Entertainment (3)                     15.  - Npm (7)                             30.  - Markdown (3)                        45.  Version Control (1)\n                01.  - Music (14)                          16.  - Boilerplate (5)                     31.  Command Line Learning (9)             46.  - Git (18)\n                02.  - Social Media (7)                    17.  Productivity (14)                     32.  Data Manipulation (1)                 47.  Images (0)\n                03.  - Video (5)                           18.  - Time Tracking (5)                   33.  - Processors (5)                      48.  - Gif Creation (7)\n                04.  - Movies (2)                          19.  - Note Taking and Lists (10)          34.  - JSON (6)                            49.  - Image Conversion (3)\n                05.  - Games (2)                           20.  - Finance (4)                         35.  - Columns (2)                         50.  - SVG (1)\n                06.  - Books (3)                           21.  - Presentations (4)                   36.  - Text (2)                            51.  Screensavers (4)\n                07.  Development (9)                       22.  - Calendars (5)                       37.  Files and Directories (0)             52.  Graphics (3)\n                08.  - Text Editors (5)                    23.  Utilities (12)                        38.  - File Managers (6)                   53.  Just for Fun (9)\n                09.  - Web Development (19)                24.  - macOS (11)                          39.  - Deleting, Copying, and Renaming (7) 54.  Other (24)\n                10.  - Mobile Development (3)              25.  - Terminal Sharing Utilities (10)     40.  - Files (10)                          55.  - Emoji (5)\n                11.  - Database (5)                        26.  - Network Utilities (6)               41.  - File Sync/Sharing (5)               56.  Other Awesome Lists (7)\n                12.  - Devops (9)                          27.  - Theming and Customization (6)       42.  - Directory Listing (4)\n                13.  - Docker (5)                          28.  - Shell Utilities (6)                 43.  - Directory Navigation (9)\n                14.  - Release (5)                         29.  - System Interaction Utilities (7)    44.  - Search (8)\n\n- 💥 Time Tracking\nTimetrap - Simple timetracker.\n🔗 https://github.com/samg/timetrap\nmoro - Simple tool for tracking work hours.\n🔗 https://github.com/omidfi/moro\nTimewarrior - Utility with simple stopwatch, calendar-based backfill and flexible reporting.\n🔗 https://github.com/GothenburgBitFactory/timewarrior\nWatson - Generate reports for clients and manage your time.\n🔗 https://github.com/TailorDev/Watson\nutt - Simple time tracking tool.\n🔗 https://github.com/larose/utt\n```\n\nShow all awesome list\n\n```\n$ awesome-cli\n✨ Entertainment\nfootball-cli - Get live scores, fixtures, standings of almost every football competition/league.\n🔗 https://github.com/ManrajGrover/football-cli\npockyt - Read, Manage, and Automate your Pocket collection.\n🔗 https://github.com/arvindch/pockyt\nnewsboat - An extendable RSS feed reader for text terminals.\n🔗 https://github.com/newsboat/newsboat\n\n- 💥 Music\ncmus - Small, fast and powerful console music player.\n...\n```\n\nShow header only\n\n```\n$ awesome-cli -k\n✨ Entertainment\n- 💥 Music\n- 💥 Social Media\n- 💥 Video\n- 💥 Movies\n- 💥 Games\n- 💥 Books\n✨ Development\n- 💥 Text Editors\n...\n```\n\nDon't show URL\n\n```\n$ awesome-cli -u\n✨ Entertainment\nfootball-cli - Get live scores, fixtures, standings of almost every football competition/league.\npockyt - Read, Manage, and Automate your Pocket collection.\nnewsboat - An extendable RSS feed reader for text terminals.\n\n- 💥 Music\ncmus - Small, fast and powerful console music player.\n...\n```\n\nInstall\n-------\n\n```\n$ python -m pip install awesome-cli\n```\n\n\nPrerequirements\n---------------\n\n* poetry\n\nBuild\n-----\n\n```\n$ poetry build\n```\n\nTODO\n----\n\n- [ ] Support multi awesome list\n- [ ] Support search\n- [ ] Support showing specific section only\n",
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
