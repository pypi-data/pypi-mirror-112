# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sec_html_parser']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4>=4.9.3,<5.0.0', 'click>=8.0.1,<9.0.0']

setup_kwargs = {
    'name': 'sec-html-parser',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Tom Selfin',
    'author_email': 'selfint@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
