# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sub_formater']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'sub-formater',
    'version': '0.1.4',
    'description': '',
    'long_description': None,
    'author': 'Will Max',
    'author_email': 'maxwillx@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.4,<4.0',
}


setup(**setup_kwargs)
