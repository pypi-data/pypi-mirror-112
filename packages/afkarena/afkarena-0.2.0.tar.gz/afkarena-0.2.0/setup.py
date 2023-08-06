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
    'version': '0.2.0',
    'description': 'Simple API wrapper for the AFK Arena site https://cdkey.lilith.com/afk-global.',
    'long_description': "# AFK Arena API.\n\nSimple API wrapper for the AFK Arena site https://cdkey.lilith.com/afk-global.\n\n> **Note:** This wrapper is unofficial and is not associated with nor endorsed by Lilith Games.\n\nThe logic of this library has been part of my Discord bot, [Dreaf](https://github.com/scragly/Dreaf), ever since AFK Arena changed to the external gift code redemption site. Due to the increased interest of community members on making use of this unofficial API, and the fact that this logic is currently being used across two seperate projects of my own, I figured it's time to make the API interactions standalone to ease maintenance and keep the feature scope focused on the essentials of its functionality.\n\n## Install\n\n```\npip install afkarena\n```\n\n## Requirements\n\n- Python 3.9+\n- aiohttp 3.7+\n\n## How to use\n\n```python\n# create a Player object for the main user account.\nplayer = Player(main_user_id)\n\n# authenticate using the authentication code in game settings.\nawait player.verify(authentication_code)\n\n# fetch data of all linked user accounts\nawait player.fetch_users()\n\n# redeem one or more gift codes for all linked user accounts\nresults = await player.redeem_codes(gift_code_one, gift_code_two)\n\n# view code redemption results\nprint(results)\n```\n",
    'author': 'scragly',
    'author_email': '29337040+scragly@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/scragly/afkarena',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
