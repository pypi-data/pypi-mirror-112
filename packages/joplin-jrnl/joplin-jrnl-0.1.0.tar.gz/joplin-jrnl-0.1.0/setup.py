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
    'version': '0.1.0',
    'description': 'An append-only journaling tool using Joplin to store the entries',
    'long_description': None,
    'author': 'Alex Kelly',
    'author_email': 'kellya@arachnitech.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
