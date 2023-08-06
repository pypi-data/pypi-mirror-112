from __future__ import annotations

import typing as t


import requests as r
from .models import Anime, Character


class AniClient(r.Session):
    def __init__(self, token: t.Optional[str] = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.token = token

    def anime(self: AniClient, name: str) -> Anime:
        return Anime(self, name)

    def character(self: AniClient, name: str):
        return Character(self, name)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, trace):
        ...
