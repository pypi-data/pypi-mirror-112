# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sf_max']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['sf = sf_max.entry:main']}

setup_kwargs = {
    'name': 'sf-max',
    'version': '0.1.1',
    'description': '',
    'long_description': None,
    'author': 'Will Max',
    'author_email': 'maxwillx@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.4,<4.0',
}


setup(**setup_kwargs)
