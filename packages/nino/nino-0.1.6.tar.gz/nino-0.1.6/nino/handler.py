from __future__ import annotations

__all__ = (
    "Query",
    "QueryHandler",
    "QueryFields",
    "QueryOperation",
    "BaseEndpoint",
)

import typing as t

from ratelimit import limits, sleep_and_retry
from .errors import HTTPException

if t.TYPE_CHECKING:
    from .client import AniClient

BASE = "https://graphql.anilist.co"


class QueryIncomplete(Exception):
    def __init__(self, element: str) -> None:
        super().__init__(f"Query missing {element!r} element")


class MISSING:
    def __init__(self):
        ...

    @staticmethod
    def build() -> str:
        "BURH"


class QueryOperation:
    def __init__(
        self, type: str, *, name: str = None, variables: t.Dict[str, str]
    ) -> None:
        self.name = name
        self.type = type
        self.variables = variables

    def build(self):
        vars = ", ".join([f"{k}: {v}" for k, v in self.variables.items()])

        if self.name:
            operation = f"{self.type} {self.name} ({vars}) "
        else:
            operation = f"{self.type} ({vars}) "

        return operation + "{"

    def __str__(self) -> str:
        return self.build()


class QueryField:
    def __init__(self, name: str, *items) -> None:
        self.name = name
        self._items = list(items)

    def add_item(self, name: str):
        self._items.append(name)
        return self

    def build(self):
        if self._items:
            items = "\n".join(self._items)
            query = self.name + " {\n" + items + "\n}"

            return query

        return self.name

    def __str__(self) -> str:
        return self.build()


class QueryFields:
    def __init__(
        self, name: str, fields: t.List[QueryField] = None, **arguments
    ) -> None:
        self.name = name
        self.fields = fields or []

        self.arguments = arguments

    def add_field(self, name: str, *items):
        field = QueryField(name, *items)
        self.fields.append(field)

        return field

    def build(self):
        if not self.fields:
            raise QueryIncomplete("fields")

        fields = "\n".join([field.build() for field in self.fields])
        args = ", ".join([f"{k}: {v}" for k, v in self.arguments.items()])

        query = f"{self.name} ({args}) " + "{\n" + fields + "\n}"
        return query

    def __str__(self) -> str:
        return self.build()


class Query:
    def __init__(
        self,
        operation: t.Union[QueryOperation, t.Type[MISSING]],
        fields: QueryFields,
    ) -> None:
        self._operation = operation
        self._fields: QueryFields = fields

    @property
    def operation(self):
        return self._operation

    @operation.setter
    def operation(self, value):
        if not isinstance(value, QueryOperation):
            raise TypeError("operation value must be an instance of QueryOperation")

        self._operation = value

    @property
    def fields(self):
        return self._fields

    @fields.setter
    def fields(self, value):
        if not isinstance(value, QueryFields):
            raise TypeError("fields value must be an instance of QueryFields")

        self._fields = value

    def set_operation(
        self, type: str, *, name: str = None, variables: t.Dict[str, str]
    ):
        operation = QueryOperation(type, name=name, variables=variables)
        self._opration = operation

        return operation

    def add_fields(
        self, name: str, fields: t.List[QueryField] = None, **arguments
    ) -> QueryFields:
        self._fields: QueryFields = QueryFields(name, fields, **arguments)

        return self._fields

    def build(self) -> str:
        if not self._operation:
            raise QueryIncomplete("operation")

        operation = self.operation.build()

        query = operation + " "
        query += self._fields.build()

        return query + "\n}"

    def __str__(self) -> str:
        return self.build()

    # <3 blanket


class QueryHandler(type):
    def __call__(cls, *args, **kwargs):
        self = type.__call__(cls, *args, **kwargs)
        cls._build_query(self)
        return self

    @sleep_and_retry
    @limits(calls=1.5, period=1)
    def _build_query(self, endpoint):
        payload = {
            "query": endpoint.query.build(),
            "variables": {
                "search": endpoint._name,
                "page": endpoint.page,
                "perPage": endpoint.per_page,
            },
        }
        resp = endpoint.client.session.post(BASE, json=payload)
        if resp.status_code != 200:
            print(resp.text)
            raise HTTPException(
                f"Status code: {resp.status_code} response: {resp.text}"
            )
        returned = resp.json()
        endpoint.data = returned["data"]


class BaseEndpoint(metaclass=QueryHandler):
    def __init__(self, client: AniClient, name: str, page: int, per_page: int):
        self.data = {}
        self.client = client
        self._name = name
        self.page = page
        self.per_page = per_page

        self.query = NotImplemented

    def __repr__(self):
        return f"<{list(self.data.keys())[0]} name={self._name}>"

    def __iter__(self):
        for key, value in self.__dict__.items():
            yield key, value
