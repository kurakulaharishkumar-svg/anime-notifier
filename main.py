"""
main.py
Entry point for the Anime WhatsApp Notifier.
Orchestrates fetching, selection, comparison, notification, and scheduling.
"""

from anime_api import fetch_anime
from selector import select_anime
from storage import load_data, get_last_notified_episode, update_episode
from notifier import send_whatsapp
from scheduler import start_scheduler
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


# ── Hardcoded anime list ──────────────────────────────────────────────
anime_list = [
    "One Piece",
    "Wistoria: Wand and Sword",
    "Liar Satsujin Game",
    "That Time I Got Reincarnated as a Slime",
    "Dr. Stone: Science Future",
    "Dorohedoro",
    "Witch Hat Atelier",
    "Classroom of the Elite",
    "The Angel Next Door Spoils Me Rotten",
    "Yomi no Tsugai",
    "Tensei Shitara Slime Datta Ken 4th Season",
    "LIAR GAME",
]


def job() -> None:
    """
    Main job: iterate over the anime list, check for new episodes,
    and send WhatsApp notifications when a new episode is detected.
    """
    print("=" * 50)
    print("[JOB] Checking for new episodes...")
    print("=" * 50)

    data = load_data()

    for title in anime_list:
        print(f"\n→ Checking: {title}")

        # 1. Fetch data from AniList
        results = fetch_anime(title)
        if results is None:
            print(f"  ⚠ Could not fetch data. Skipping.")
            continue

        # 2. Select the correct anime
        anime = select_anime(results)
        if anime is None:
            print(f"  ℹ Not currently airing or no upcoming episode. Skipping.")
            continue

        # 3. Extract episode info
        next_ep = anime.get("nextAiringEpisode")
        if next_ep is None:
            print(f"  ℹ No next airing episode found. Skipping.")
            continue

        episode = next_ep.get("episode")
        if episode is None:
            print(f"  ℹ Episode number missing. Skipping.")
            continue

        romaji = anime.get("title", {}).get("romaji", title)
        cover_url = anime.get("coverImage", {}).get("large", "")

        # 4. Compare with stored data
        last_ep = get_last_notified_episode(data, romaji)

        if episode > last_ep:
            print(f"  🔥 New episode detected! Ep {episode} (last notified: {last_ep})")

            # 5. Send WhatsApp notification
            success = send_whatsapp(romaji, episode, cover_url)

            if success:
                # 6. Update storage
                update_episode(data, romaji, episode)
                print(f"  ✅ Notified and saved.")
            else:
                print(f"  ❌ WhatsApp failed. Will retry next cycle.")
        else:
            print(f"  ✔ Already notified for Ep {last_ep}. Nothing new.")

    print("\n[JOB] Done.\n")


if __name__ == "__main__":
    start_scheduler(job)
