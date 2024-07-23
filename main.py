import requests
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta, timezone

load_dotenv()

client_id = os.getenv("TWITCH_CLIENT_ID")
client_secret = os.getenv("TWITCH_SECRET")
access_token = ""


def get_token():
    global access_token
    url = "https://id.twitch.tv/oauth2/token"
    payload = {
        "client_id": client_id,
        "client_secret": client_secret,
        "grant_type": "client_credentials",
    }
    response = requests.post(url, data=payload)
    if response.status_code == 200:
        data = response.json()
        print("Connected to Twitch")
        access_token = data["access_token"]
    else:
        print("Could not connect to Twitch")


def get_headers():
    return {"Client-Id": client_id, "Authorization": f"Bearer {access_token}"}


def format_datetime(dt):
    return dt.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"


def get_tarkov_clips():
    now = datetime.now(timezone.utc)
    time_24_hours_ago = now - timedelta(hours=24)
    formatted_now = format_datetime(now)
    formatted_24_hours_ago = format_datetime(time_24_hours_ago)

    response = requests.get(
        f"https://api.twitch.tv/helix/clips?game_id=491931&started_at={formatted_24_hours_ago}&ended_at={formatted_now}",
        headers=get_headers(),
    )
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to get clips: {response.status_code}")
        return None


def main():
    get_token()
    clips = get_tarkov_clips()
    if clips:
        english_clips = [clip for clip in clips["data"] if clip.get("language") == "en"]
        print(english_clips)


if __name__ == "__main__":
    main()
