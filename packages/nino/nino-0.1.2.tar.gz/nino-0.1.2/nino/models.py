from __future__ import annotations


import typing as t
from ratelimit import limits, sleep_and_retry
from .constants import ANIME_QUERY, CHARACTER_QUERY, BASE


if t.TYPE_CHECKING:
    from .client import AniClient

from .errors import HTTPException


class QueryHandler(type):
    def __call__(cls, *args, **kwargs):
        self = type.__call__(cls, *args, **kwargs)
        resp = self._build_query()
        return self


class BaseEndpoint(object, metaclass=QueryHandler):
    def __init__(self, client: AniClient, name: str):
        self.data = {}
        self.client = client
        self._name = name

        self.QUERY = NotImplemented

    @sleep_and_retry
    @limits(calls=1.5, period=1)
    def _build_query(self):
        payload = {
            "query": self.QUERY,
            "variables": {"search": self._name},
        }
        resp = self.client.post(BASE, json=payload)
        if resp.status_code != 200:
            print(resp.text)
            raise HTTPException(
                f"Status code: {resp.status_code} response: {resp.text}"
            )
        returned = resp.json()
        self.data = returned["data"]

    def __repr__(self):
        return f"<name={self._name}, type={list(self.data.keys())[0]}>"

    def __iter__(self):
        for key, value in self.__dict__.items():
            yield key, value


class Anime(BaseEndpoint):
    def __init__(self, client: AniClient, name: str):
        super().__init__(client, name)
        self.QUERY = ANIME_QUERY
        self.client = client

    @property
    def id(self):
        return self.data["Media"]["id"]

    @property
    def title(self):
        return self.data["Media"]["title"]

    @property
    def description(self):
        return self.data["Media"]["description"]

    @property
    def averageScore(self):
        return self.data["Media"]["averageScore"]

    @property
    def status(self):
        return self.data["Media"]["status"]

    @property
    def tags(self):
        return [tag["name"] for tag in self.data["Media"]["tags"]]


class Character(BaseEndpoint):
    def __init__(self, client: AniClient, name: str):
        super().__init__(client, name)
        self.QUERY = CHARACTER_QUERY
        self.client = client

    @property
    def name(self):
        return self.data["Character"]["name"]

    @property
    def description(self):
        return self.data["Character"]["description"]

    @property
    def image(self):
        return self.data["Character"]["image"]
