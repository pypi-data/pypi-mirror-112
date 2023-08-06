# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aiohttp_rpc',
 'aiohttp_rpc.client',
 'aiohttp_rpc.protocol',
 'aiohttp_rpc.server']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.7.3,<4.0.0']

setup_kwargs = {
    'name': 'aiohttp-rpc',
    'version': '0.7.2',
    'description': '',
    'long_description': None,
    'author': 'expert-m',
    'author_email': 'michael@sulyak.info',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.5,<4.0.0',
}


setup(**setup_kwargs)
