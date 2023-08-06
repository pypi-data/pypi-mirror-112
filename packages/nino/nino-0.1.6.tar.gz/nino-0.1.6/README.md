# Basic usage

Character
```py
from nino import AniClient

with AniClient() as client:
    character = client.character("Momonga")
    print(character.name)

```

Anime
```py
from nino import AniClient

with AniClient() as client:
    anime = client.anime("Overlord")
    print(anime.title)

```