import requests
import time
import json
from datetime import datetime
import os

GROUP_ID = 976
ACHIEVEMENTS_URL = f"https://api.wiseoldman.net/v2/groups/{GROUP_ID}/achievements"
DISCORD_WEBHOOK_URL = os.environ["DISCORD_WEBHOOK_URL"]
LAST_SEEN_FILE = "last_achievement.json"

print("Waiting 5 minutes to let WOM update.")
time.sleep(300)  # 5 minutes

def fetch_achievements():
    response = requests.get(ACHIEVEMENTS_URL)
    return response.json()

def get_last_seen():
    try:
        with open(LAST_SEEN_FILE, "r") as f:
            return f.read().strip()
    except FileNotFoundError:
        return None

def save_last_seen(ts):
    with open(LAST_SEEN_FILE, "w") as f:
        f.write(ts)

def send_to_discord(achievements):
    for ach in achievements:
        player = ach["playerName"]
        metric = ach["metric"]
        type_ = ach["type"]
        date = ach["createdAt"][:10]
        msg = f"**{player}** achieved **{type_.capitalize()} {metric.capitalize()}**!"
        print(f"Sending: {msg}")
        requests.post(DISCORD_WEBHOOK_URL, json={"content": msg})

def main():
    last_seen = get_last_seen()
    achievements = fetch_achievements()

    new_achievements = []
    for ach in achievements:
        ts = ach["createdAt"]
        if ts == last_seen:
            break
        new_achievements.append(ach)

    if new_achievements:
        new_achievements.reverse()
        send_to_discord(new_achievements)
        save_last_seen(new_achievements[-1]["createdAt"])
    else:
        print("✅ No new achievements found.")

main()
