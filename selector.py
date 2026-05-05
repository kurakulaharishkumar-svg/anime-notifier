"""
selector.py
Selects the correct anime from AniList search results.
"""


def select_anime(results: list) -> dict | None:
    """
    From a list of AniList media results, pick the first anime that is
    currently RELEASING and has a nextAiringEpisode.

    Args:
        results: List of media dicts from AniList API.

    Returns:
        The matching media dict, or None if no match found.
    """
    if not results:
        return None

    for anime in results:
        status = anime.get("status")
        next_ep = anime.get("nextAiringEpisode")

        if status == "RELEASING" and next_ep is not None:
            return anime

    return None
