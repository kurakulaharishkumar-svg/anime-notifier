"""
notifier.py
Sends WhatsApp notifications via the Twilio API.
"""

import os
from twilio.rest import Client


def send_whatsapp(title: str, episode: int, cover_url: str) -> bool:
    """
    Send a WhatsApp message with anime episode info and cover image.

    Args:
        title:     The anime title (romaji).
        episode:   The new episode number.
        cover_url: URL of the anime cover image.

    Returns:
        True if the message was sent successfully, False otherwise.
    """
    account_sid = os.environ.get("TWILIO_ACCOUNT_SID")
    auth_token = os.environ.get("TWILIO_AUTH_TOKEN")
    from_number = os.environ.get("FROM_WHATSAPP_NUMBER")
    to_number = os.environ.get("TO_WHATSAPP_NUMBER")

    if not all([account_sid, auth_token, from_number, to_number]):
        print("[ERROR] Missing Twilio environment variables.")
        return False

    body = f"Hey Harish 👋\n{title} Episode {episode} is out 🔥"

    try:
        client = Client(account_sid, auth_token)
        message = client.messages.create(
            body=body,
            from_=f"whatsapp:{from_number}",
            to=f"whatsapp:{to_number}",
            media_url=[cover_url],
        )
        print(f"[OK] WhatsApp sent for {title} Ep {episode} (SID: {message.sid})")
        return True

    except Exception as e:
        print(f"[ERROR] Failed to send WhatsApp for '{title}': {e}")
        return False
