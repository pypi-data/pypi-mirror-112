# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aiobungie',
 'aiobungie.ext',
 'aiobungie.objects',
 'aiobungie.types',
 'aiobungie.utils']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.7.4,<4.0.0', 'python-dateutil>=2.8.1,<3.0.0']

setup_kwargs = {
    'name': 'aiobungie',
    'version': '0.2.4',
    'description': 'A small async api wrapper for the bungie api',
    'long_description': "# aiobungie\n\nAn Asynchronous statically typed API wrapper for the bungie API written in Python.\n\n# Features\n\n* Fully Asynchronous.\n* Easy to use.\n* Statically typings and annotations.\n* All endpoints will be implemented.\n\n# Installing\n\nOfficial release.\n\n```s\n$ pip install aiobungie\n```\n\nDevelopment\n\n```s\n$ pip install git+https://github.com/nxtlo/aiobungie\n```\n\n## Quick Example\n\n```python\nimport aiobungie\n\nclient = aiobungie.Client(key='YOUR_API_KEY')\n\nasync def main() -> None:\n\n    # fetch a clan.\n    clan = await client.fetch_clan(1234)\n    print(f'{clan.id}, {clan.name}, {clan.owner}, {clan.created_at}, {clan.about}')\n\n    # fetch a bungie user.\n    player = await client.fetch_player('Fate怒')\n    print(f'{player.name}, {player.id[0]}, {player.icon}, {player.type}')\n\n    # fetch a specific character.\n    char = await client.fetch_character(player.id[0], aiobungie.MembershipType.STEAM, aiobungie.DestinyCharacter.WARLOCK)\n    print(f'{char.emblem}, {char.light}, {char.id}, {char.race}, {char.gender}, {char._class}')\n\n    # fetch activities.\n    activ = await client.fetch_activity(player.id[0], char.id, aiobungie.MembershipType.STEAM, aiobungie.GameMode.RAID)\n    print(\n        f'''{activ.mode}, {activ.kills}, {activ.player_count}, \n        {activ.duration}, {activ.when}, {activ.kd}, {activ.deaths},\n        {activ.assists}, {activ.hash} -> raids only {activ.raw_hash} -> Any\n        ''')\n\n    # Raw search\n    endpoint = await client.from_path('User/.../.../')\n    print(endpoint)\n\nclient.loop.run_until_complete(main())\n```\n\n## OAuth2\n\n```py\n# OAuth2 is not fully implemented yet.\n\nfrom aiobungie.ext import OAuth2, refresh\n\nclient = OAuth2(token='', secret='')\n\n# Use the refresh decorator to automatically refresh the tokens\n# The cls param is required to get the client secret and pass it to the POST request.\n\n@refresh(hours=1, cls=client)\nasync def auth_stuff() -> None:\n    await client.do_auth()\n    print(await client.get_current_user())\n\nclient.loop.run_until_complete(auth_stuff())\n```\n\n### Requirements\n* Python >=3.8\n* aiohttp\n\n### OAuth2 and Dev\n* cryptography\n* requests_oauthlib\n* aiosqlite\n* aiofiles\n* python-dotenv\n\n\n### Getting Help\n* Discord: `Fate 怒#0008`\n* Docs: Soon.",
    'author': 'nxtlo',
    'author_email': 'dhmony-99@hotmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/nxtlo/aiobungie',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
