from __future__ import annotations

__all__ = "AniClient"

from typing import Optional

import requests as r
from .endpoints import Anime, Character


class AniClient:
    def __init__(self, token: Optional[str] = None, session: Optional[r.Session] = None, *args, **kwargs):
        """
        AniClient Constructor.

        Args:
            token: Your Anilist API token.
            session: The session used to send requests
        """
        super().__init__(*args, **kwargs)
        self.token = token
        self.session = session or r.Session()

    def anime(self: AniClient, name: str, page: int = 1, per_page: int = 1) -> Anime:
        """
        This method is used to create an `Anime` instance.

        Args:
            name: The name of the anime being searched.
            page: The page to show for the search.
            per_page: Amount of results shown per page.

        Returns:
            The [Anime](./anime.md) instance that was created.
        """
        return Anime(self, name, page, per_page)

    def character(
        self: AniClient, name: str, page: int = 1, per_page: int = 1
    ) -> Character:
        """
        This method is used to create a Character instance.

        Args:
            name: The name of the character being searched.
            page: The page to show for the search.
            per_page: Amount of results shown per page.

        Returns:
            The [Character](./character.md) instance that was created.
        """
        return Character(self, name, page, per_page)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, trace):
        self.session.close()
