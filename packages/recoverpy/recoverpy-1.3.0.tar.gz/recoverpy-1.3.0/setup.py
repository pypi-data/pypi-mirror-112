# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['recoverpy', 'recoverpy.views']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=5.4.1,<6.0.0', 'py-cui>=0.1.3,<0.2.0']

setup_kwargs = {
    'name': 'recoverpy',
    'version': '1.3.0',
    'description': 'A TUI to recover overwritten or deleted data.',
    'long_description': '<div align="center">\n    <img src="docs/assets/logo.png" alt="RecoverPy">\n</div>\n\n<p align="center">\n    <em>Recover overwritten or deleted data.</em>\n</p>\n\n<p align="center">\n<a href="https://img.shields.io/github/v/release/pablolec/recoverpy" target="_blank">\n    <img src="https://img.shields.io/github/v/release/pablolec/recoverpy" alt="Release">\n</a>\n<a href="https://github.com/PabloLec/recoverpy/blob/main/LICENSE" target="_blank">\n    <img src="https://img.shields.io/github/license/pablolec/recoverpy" alt="License">\n</a>\n<a href="https://pepy.tech/project/recoverpy" target="_blank">\n    <img src="https://static.pepy.tech/personalized-badge/recoverpy?period=total&units=abbreviation&left_color=grey&right_color=red&left_text=Download" alt="Downloads">\n</a>\n<a href="#" target="_blank">\n    <img src="https://github.com/PabloLec/recoverpy/actions/workflows/recoverpy-tests.yml/badge.svg?branch=main" alt="Tests">\n</a>\n</p>\n\n---\n\n# RecoverPy\n\nRecoverPy is a TUI utility written in Python with the help of [py_cui](https://github.com/jwlodek/py_cui "py_cui").\n\nYou can already find plenty of solutions to recover deleted files but it can be a hassle to recover overwritten files. RecoverPy searches through every inodes to find your request.\n\n\n\n## Demo\n\n<p align="center">\n    <img src="docs/assets/demo.gif">\n</p>\n\n## Installation\n\n:penguin: The main prerequisite is having a Linux system.\n\n**Mandatory:** To list and search through your partitions, recoverpy uses `grep`, `dd`, and `lsblk` commands.  \n**Optional:** To display real time grep progress, you can install `progress` tool.\n\nTo install all dependencies:\n- Debian-like: `apt install grep coreutils util-linux progress`  \n- Arch: `pacman -S grep coreutils util-linux progress`  \n- Fedora: `dnf install grep coreutils util-linux progress`  \n\n**Installation from pip**: `python3 -m pip install recoverpy`  \n\n*Pip should be already installed if you have Python >=3.4. Otherwise, see [\npip docs](https://pip.pypa.io/en/stable/installing/ "pip docs") for installation.*\n\nTo update: `python3 -m pip install --upgrade recoverpy`\n\n## Usage\n\n```bash\npython3 -m recoverpy\n```\n\n**You must have root access to use recoverpy**.\n\nIf you are not logged as root use `sudo recoverpy` or log in with `su -` before execution.\n\nFirst, **select the system partition** in which your file was. If you are out of luck, you can alternatively search in your home partition, maybe your IDE, text editor, etc. made a backup at some point.\n\nThen, **type a text to search**. You can now start the search.\n\nNote that searching a string in a whole partition may take _a while_. (see [euphemism](https://en.wikipedia.org/wiki/Euphemism "euphemism"))\n\nResults will appear in the left-hand box. Select a result to display the corresponding partition block content in the right-hand box.\n\nOnce you have found your precious, select `Save`.\nYou can now either save this block individually or explore neighboring blocks for the remaining parts of the file. You could then save it all in one file.\n\n**Save path is set in `conf.yaml`. Default is `/tmp/`.**\n\n## Tips\n\n- Always do backups! Yes, maybe too late...\n- **Unmount your partition before you do anything!** Although you can search with your partition still mounted, it is highly recommended to unmount your partition to avoid any alteration to your file.\n\nRegarding the string you search:\n\n- Be concise, find something that could be unique to your file.\n- Stay simple, your string is escaped but exotic characters may affect your results.\n- Try to remember the last edit you have made to your file.\n\nWhen you have a match:\n\n- Use the option to explore neighboring blocks to make sure you do not miss some part of your file.\n',
    'author': 'PabloLec',
    'author_email': 'pablo.lecolinet@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/PabloLec/recoverpy',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
