# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sub_formater']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['subformater = entry:main']}

setup_kwargs = {
    'name': 'sub-formater',
    'version': '0.1.0',
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
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
