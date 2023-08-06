from __future__ import annotations

__all__ = ("Anime", "Character")

import pathlib
from typing import Union, TYPE_CHECKING, Dict, Optional
from .handler import BaseEndpoint
from .queries import AnimeQ, CharacterQ

if TYPE_CHECKING:
    from .client import AniClient


class Image:
    def __init__(self, client: AniClient, payload: Union[Dict[str, str], str]) -> None:
        self._client = client
        try:
            if isinstance(payload, str):
                self._large: Optional[str] = payload
                self._medium: Optional[str] = None
            else:
                self._large = payload.get("large")
                self._medium = payload.get("medium")
        except AttributeError:
            pass

    @property
    def large(self) -> Optional[str]:
        """
        Returns:
            High resolution image.
        """
        return self._large

    @property
    def medium(self) -> Optional[str]:
        """
        Returns:
            Medium resolution image.
        """
        return self._medium

    def read(self, large: bool = True, medium: bool = False) -> bytes:
        """
        Reads the image.

        Args:
            large: Whether to read `large` image.
            medium: Whether to read `medium` image.

        Returns:
            image's bytes.
        """
        if large and medium:
            raise ValueError("Cannot set both large and medium to True")

        if not large and not medium:
            raise ValueError("Cannot set both large and medium to False")

        if large:
            url = self.large

        if medium:
            url = self.medium

        resp = self._client.get(url)
        return resp.content

    def save(self, fp: Union[str, pathlib.Path], *, large: bool = True, medium: bool = False) -> int:
        """
        Saves the image.

        Args:
            fp: file-path with file name and extension.
            large: Whether to save `large` image.
            medium: Whether to save `medium` image.

        Returns:
            Number of bytes written.
        """
        data = self.read(large=large, medium=medium)

        with open(fp, "wb") as file:
            return file.write(data)


class Anime(BaseEndpoint):
    def __init__(self, client: AniClient, name: str, page: int, per_page: int):
        super().__init__(client, name, page, per_page)
        self.query = AnimeQ
        self.client = client
        self.page = page
        self.per_page = per_page

    @property
    def title(self) -> Union[dict, list]:
        """
        Returns:
            A dict or list of dicts of anime titles.
        """
        if self.per_page == 1:
            return self.data["Page"]["media"][0]["title"]
        else:
            return [anime["title"] for anime in self.data["Page"]["media"]]

    @property
    def description(self) -> Union[str, list]:
        """
        Returns:
            A string or list of string of anime descriptions.
        """
        if self.per_page == 1:
            return self.data["Page"]["media"][0]["description"]
        else:
            return [anime["description"] for anime in self.data["Page"]["media"]]

    @property
    def average_score(self) -> Union[int, list]:
        """
        Returns:
            An integer or list of integers of average anime scores.
        """
        if self.per_page == 1:
            return self.data["Page"]["media"][0]["averageScore"]
        else:
            return [anime["averageScore"] for anime in self.data["Page"]["media"]]

    @property
    def status(self) -> Union[str, list]:
        """
        Returns:
            A string or list of strings of anime statuses.
        """
        if self.per_page == 1:
            return self.data["Page"]["media"][0]["status"]
        else:
            return [anime["status"] for anime in self.data["Page"]["media"]]

    @property
    def episodes(self) -> Union[int, list]:
        """
        Returns:
            An integer or list of integers of number of episodes.
        """
        if self.per_page == 1:
            return self.data["Page"]["media"][0]["episodes"]
        else:
            return [anime["episodes"] for anime in self.data["Page"]["media"]]

    @property
    def url(self) -> Union[str, list]:
        """
        Returns:
            A string or list of strings of anime webpage urls.
        """
        if self.per_page == 1:
            return self.data["Page"]["media"][0]["siteUrl"]
        else:
            return [anime["siteUrl"] for anime in self.data["Page"]["media"]]

    @property
    def cover_image(self) -> Union[str, list]:
        """
        Returns:
            A string or list of [Image](./image.md)s of anime's cover images.
        """
        if self.per_page == 1:
            return self.data["Page"]["media"][0]["coverImage"]
        else:
            return [
                Image(self.client, anime["coverImage"])
                for anime in self.data["Page"]["media"]
            ]

    @property
    def banner_image(self) -> Union[str, list]:
        """
        Returns:
            A string or list of [Image](./image.md)s with anime's banner images.
        """
        if self.per_page == 1:
            return self.data["Page"]["media"][0]["bannerImage"]
        else:
            print(self.data["Page"]["media"][0]["bannerImage"])
            return [
                Image(self.client, anime["bannerImage"])
                for anime in self.data["Page"]["media"]
            ]

    @property
    def tags(self) -> list:
        """
        Returns:
            A list or list of lists of anime tags.
        """
        if self.per_page == 1:
            return [tag["name"] for tag in self.data["Page"]["media"][0]["tags"]]
        else:
            tags = []
            for anime in self.data["Page"]["media"]:
                tags.append(
                    [tag["name"] for tag in self.data["Page"]["media"][0]["tags"]]
                )
            return tags


class Character(BaseEndpoint):
    def __init__(self, client: AniClient, name: str, page: int, per_page: int):
        super().__init__(client, name, page, per_page)
        self.query = CharacterQ
        self.client = client
        self.page = page
        self.per_page = per_page

    @property
    def name(self) -> Union[dict, list]:
        """
        Returns:
            A dict or list of dicts of character names.
        """
        if self.per_page == 1:
            return self.data["Page"]["characters"][0]["name"]
        else:
            return [char["name"] for char in self.data["Page"]["characters"]]

    @property
    def description(self) -> Union[str, list]:
        """
        Returns:
            A string or list of strings of character descriptions.
        """
        if self.per_page == 1:
            return self.data["Page"]["characters"][0]["description"]
        else:
            return [char["description"] for char in self.data["Page"]["characters"]]

    @property
    def age(self) -> Union[str, list]:
        """
        Returns:
            A string or list of strings of character ages.
        """
        if self.per_page == 1:
            return self.data["Page"]["characters"][0]["age"]
        else:
            return [char["age"] for char in self.data["Page"]["characters"]]

    @property
    def url(self) -> Union[str, list]:
        """
        Returns:
            A string or list of strings of character's webpage url.
        """
        if self.per_page == 1:
            return self.data["Page"]["characters"][0]["siteUrl"]
        else:
            return [char["siteUrl"] for char in self.data["Page"]["characters"]]

    @property
    def gender(self) -> Union[str, list]:
        """
        Returns:
            A string or list of strings of character genders.
        """
        if self.per_page == 1:
            return self.data["Page"]["characters"][0]["gender"]
        else:
            return [char["gender"] for char in self.data["Page"]["characters"]]

    @property
    def date_of_birth(self) -> Union[dict, list]:
        """
        Returns:
            A dict or list of dicts of character date-of-births.
        """
        if self.per_page == 1:
            return self.data["Page"]["characters"][0]["dateOfBirth"]
        else:
            return [char["dateOfBirth"] for char in self.data["Page"]["characters"]]

    @property
    def image(self) -> Union[Image, list]:
        """
        Returns:
            A string or list of [Image](./image.md)s with character images.
        """
        if self.per_page == 1:
            return Image(self.client, self.data["Page"]["characters"][0]["image"])
        else:
            return [
                Image(self.client, char["image"])
                for char in self.data["Page"]["characters"]
            ]
