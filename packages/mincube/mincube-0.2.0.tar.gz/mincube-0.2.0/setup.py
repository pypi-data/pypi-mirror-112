# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mincube']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['my-script = minimum_cubes.getCubes:minCubes']}

setup_kwargs = {
    'name': 'mincube',
    'version': '0.2.0',
    'description': '',
    'long_description': None,
    'author': 'Vivek Pandit',
    'author_email': 'vivek.pandit@outlook.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
