# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nd_math']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'nd-math',
    'version': '0.1.1',
    'description': 'Math package for Numerical Design company',
    'long_description': None,
    'author': 'NumDes',
    'author_email': 'info@numdes.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
