from .handler import Query, QueryOperation, QueryFields

__all__ = ("AnimeQ", "CharacterQ")


extra_fields = (
    "title {romaji english native}"
    + " description averageScore status episodes siteUrl"
    + " coverImage {large medium}"
    + " bannerImage tags {name}"
)

operation = QueryOperation(
    "query", variables={"$page": "Int", "$perPage": "Int", "$search": "String"}
)
fields = QueryFields("Page", page="$page", perPage="$perPage")
fields.add_field(
    "pageInfo", "total", "currentPage", "lastPage", "hasNextPage", "perPage"
)
fields.add_field("media (search: $search, type: ANIME)", extra_fields)
AnimeQ = Query(operation=operation, fields=fields)

extra_fields = (
    "name {first last}"
    + " dateOfBirth {year month day}"
    + " age siteUrl description gender"
    + " image {large medium}"
)

operation = QueryOperation(
    "query", variables={"$page": "Int", "$perPage": "Int", "$search": "String"}
)
fields = QueryFields("Page", page="$page", perPage="$perPage")
fields.add_field(
    "pageInfo", "total", "currentPage", "lastPage", "hasNextPage", "perPage"
)
fields.add_field("characters (search: $search)", extra_fields)
CharacterQ = Query(operation=operation, fields=fields)
