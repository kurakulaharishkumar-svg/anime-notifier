"""
storage.py
Handles reading and writing the data.json persistence file.
"""

import json
import os

DATA_FILE = os.path.join(os.path.dirname(__file__), "data.json")


def load_data() -> dict:
    """
    Load the stored episode data from data.json.
    Creates an empty dict if the file does not exist or is invalid.

    Returns:
        A dict mapping anime titles to their last-notified episode number.
    """
    if not os.path.exists(DATA_FILE):
        return {}

    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        print(f"[WARN] Could not read {DATA_FILE}, starting fresh: {e}")
        return {}


def save_data(data: dict) -> None:
    """
    Save updated episode data back to data.json.

    Args:
        data: Dict mapping anime titles to last-notified episode numbers.
    """
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    except IOError as e:
        print(f"[ERROR] Could not write to {DATA_FILE}: {e}")


def get_last_notified_episode(data: dict, title: str) -> int:
    """
    Get the last episode number we notified about for a given anime.

    Args:
        data:  The loaded data dict.
        title: The anime title key.

    Returns:
        The episode number (int), or 0 if not found.
    """
    return data.get(title, 0)


def update_episode(data: dict, title: str, episode: int) -> None:
    """
    Update the stored episode for an anime and persist to disk.

    Args:
        data:    The loaded data dict (mutated in place).
        title:   The anime title key.
        episode: The new episode number.
    """
    data[title] = episode
    save_data(data)
