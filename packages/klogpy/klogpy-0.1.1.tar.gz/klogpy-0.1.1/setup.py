# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['klogpy']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0', 'colorama>=0.4.4,<0.5.0', 'parsy>=1.3,<2.0']

entry_points = \
{'console_scripts': ['klogpy = klogpy.cli:klg']}

setup_kwargs = {
    'name': 'klogpy',
    'version': '0.1.1',
    'description': 'Python implementation of klog format for time tracking',
    'long_description': None,
    'author': 'Nick Yu',
    'author_email': 'nickyu42@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
