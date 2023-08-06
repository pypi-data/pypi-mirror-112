# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['afkarena']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.7.4,<4.0.0']

setup_kwargs = {
    'name': 'afkarena',
    'version': '0.1.0',
    'description': 'Simple API wrapper for the AFK Arena site https://cdkey.lilith.com/afk-global.',
    'long_description': None,
    'author': 'scragly',
    'author_email': '29337040+scragly@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
