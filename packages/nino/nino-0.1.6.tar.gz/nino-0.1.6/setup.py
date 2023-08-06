# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nino']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.7.4,<4.0.0', 'ratelimit>=2.2.1,<3.0.0', 'requests>=2.25.1,<3.0.0']

setup_kwargs = {
    'name': 'nino',
    'version': '0.1.6',
    'description': 'A small unofficial AniList API wrapper made for python',
    'long_description': '# Basic usage\n\nCharacter\n```py\nfrom nino import AniClient\n\nwith AniClient() as client:\n    character = client.character("Momonga")\n    print(character.name)\n\n```\n\nAnime\n```py\nfrom nino import AniClient\n\nwith AniClient() as client:\n    anime = client.anime("Overlord")\n    print(anime.title)\n\n```',
    'author': 'Andy',
    'author_email': 'yrisxl@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/an-dyy/nino',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
