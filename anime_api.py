"""
anime_api.py
Fetches anime data from AniList GraphQL API.
"""

import requests


ANILIST_URL = "https://graphql.anilist.co"

QUERY = """
query ($search: String) {
  Page(perPage: 5) {
    media(search: $search, type: ANIME) {
      id
      title {
        romaji
      }
      status
      coverImage {
        large
      }
      nextAiringEpisode {
        episode
        airingAt
      }
    }
  }
}
"""


def fetch_anime(search_title: str) -> list | None:
    """
    Fetch anime search results from AniList.

    Args:
        search_title: The anime title to search for.

    Returns:
        A list of media results, or None on failure.
    """
    variables = {"search": search_title}

    try:
        response = requests.post(
            ANILIST_URL,
            json={"query": QUERY, "variables": variables},
            timeout=15,
        )
        response.raise_for_status()
        data = response.json()
        return data.get("data", {}).get("Page", {}).get("media", [])

    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Failed to fetch data for '{search_title}': {e}")
        return None
