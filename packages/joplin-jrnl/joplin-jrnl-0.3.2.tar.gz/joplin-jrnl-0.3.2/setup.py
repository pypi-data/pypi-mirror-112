# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': '.'}

packages = \
['joplin_jrnl']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=5.4.1,<6.0.0', 'click>=8.0.1,<9.0.0', 'requests>=2.25.1,<3.0.0']

entry_points = \
{'console_scripts': ['jj = joplin_jrnl.main:main']}

setup_kwargs = {
    'name': 'joplin-jrnl',
    'version': '0.3.2',
    'description': 'An append-only journaling tool using Joplin to store the entries',
    'long_description': '# Joplin-jrnl\nThis is a CLI to append notes to a notebook as a running, append-only journaling system.  The general inspiration was the [jrnl](https://jrnl.sh/en/stable/) command line tool.  I like the general simplicity of how it works, but wanted the data to be more accessible through Joplin, which I use for general notetaking.\n\n# How the heck do I use this?\njoplin-jrnl has been published to PyPi, so you should be able to get this\nrunning by simply executing `pip install joplin-jrnl`.  You may then run the\n`jj` command to see how to further interact with it.\n\nThis is an early development version, as such there aren\'t many sanity checks in\nplace.  So at the moment you have to create an area for the configuration to\nlive and there is currently no option to specify an alternate location (I\'ll get\nthere ;) )\n\n## Create a note in joplin that will serve as your journal\nIn order for the script to work, you must have a note designated as the journal.\nTo do this:\n\n    1. Open Joplin\n    2. Create a note (you can name it anything you wish)\n    3. Right click the note and select "copy markdown link"\n    4. You will get a value like "[note-name](:/df36fc8138da4169b29f0a577cba601e)  You need to paste in just the \'df36fc8138da4169b29f0a577cba601e\' part as the note id in ~/.config/jj/conf.yaml.\n\n## create configuration file and path\n\n    1. `mkdir ~/.config/joplin-jrnl/`\n    2. `cp conf.yaml ~/.config/joplin-jrnl/`\n    3. Edit conf.yaml to reflect your values\n\n# demo\n[![Demonstration](https://asciinema.org/a/WQp9Udq9vq3of9zSToqfByJxf.svg)](https://asciinema.org/a/WQp9Udq9vq3of9zSToqfByJxf)\n\n# Roadmap/Hopes and Dreams\n- [x] Add entries to a joplin note\n- [x] Optionally use editor to make bigger edits (or to deal with annoying\n    characters in entry that shell wants to expand to something\n- [ ] Search for entries based on content\n- [ ] Search for entries based on tags\n- [x] More intelligent handling of options\n    - [ ] Create a note if you don\'t specify one\n    - [ ] Utilize options to override settings\n- [x] Print out entries to CLI\n- [ ] Basically work like jrnl, but with joplin :)\n- [ ] Figure out asyncio stuff and use that instead of requests\n',
    'author': 'Alex Kelly',
    'author_email': 'kellya@arachnitech.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/kellya/joplin-jrnl',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
