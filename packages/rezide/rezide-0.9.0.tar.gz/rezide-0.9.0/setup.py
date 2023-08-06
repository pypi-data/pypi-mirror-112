# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['rezide', 'rezide.utils']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0.0,<9.0.0', 'i3ipc>=2.2.1,<3.0.0', 'toml>=0.10.2,<0.11.0']

entry_points = \
{'console_scripts': ['get-tree = rezide.get_tree:main',
                     'get-window-sizes = rezide.get_window_sizes:main',
                     'rzd = rezide.rezide:main']}

setup_kwargs = {
    'name': 'rezide',
    'version': '0.9.0',
    'description': '',
    'long_description': None,
    'author': 'abstractlyZach',
    'author_email': 'zach3lee@gmail.com',
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
