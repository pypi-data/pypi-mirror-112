ANIME_QUERY = """
query ($search: String) {
  Media (search: $search, type: ANIME) {
    title {
      romaji
      english
      native
    }
    description
    averageScore
    status
    tags{
      name
    }
  }
}
"""

CHARACTER_QUERY = """
query ($search: String) {
  Character(search: $search) {
    id
    name {
      first
      last
    }
    description
    image {
      large
    }
  }
}
"""

BASE = "https://graphql.anilist.co"
