import os
import json
import time
import requests
from headline_helper import get_daily_header #Import function that generates a date + headline string.

#Get Discord webhook URL from environment variable stored in your github repository secrets.
DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")

#Define metrics to help interpret achievements in the discord message.
SKILLS = ['attack', 'defence', 'strength', 'hitpoints', 'ranged', 'prayer', 'magic', 'cooking', 'woodcutting', 'fletching', 'fishing', 'firemaking', 'crafting', 'smithing', 'mining', 'herblore', 'agility', 'thieving', 'slayer', 'farming', 'runecrafting', 'hunter', 'construction']
BOSSES = {'abyssal-sire', 'mimic', 'tzkal-zuk', 'giant-mole', 'theatre-of-blood-hard-mode', 'venenatis', 'hespori', 'kalphite-queen', 'grotesque-guardians', 'phosanis-nightmare', 'sarachnis', 'the-gauntlet', 'the-corrupted-gauntlet', 'kraken', 'barrows-chests', 'dagannoth-supreme', 'skotizo', 'scorpia', 'callisto', 'crazy-archaeologist', 'king-black-dragon', 'tempoross', 'alchemical-hydra', 'theatre-of-blood', 'vorkath', 'general-graardor', 'chambers-of-xeric', 'bryophyta', 'commander-zilyana', 'dagannoth-rex', 'obor', 'wintertodt', 'dagannoth-prime', 'chambers-of-xeric-challenge-mode', 'kril-tsutsaroth', 'tztok-jad', 'corporeal-beast', 'vetion', 'zulrah', 'nex', 'kree-ara', 'deranged-archaeologist', 'thermonuclear-smoke-devil', 'chaos-elemental', 'nightmare', 'zalcano', 'cerberus', 'chaos-fanatic'}
CLUES = {'clue_scroll_all': 'All', 'clue_scroll_beginner': 'Beginner', 'clue_scroll_easy': 'Easy', 'clue_scroll_medium': 'Medium', 'clue_scroll_hard': 'Hard', 'clue_scroll_elite': 'Elite', 'clue_scroll_master': 'Master'}
ACTIVITIES = ['last-man-standing', 'pvp-arena', 'soul-wars-zeal', 'guardian-defence', 'rifts-closed']

#Format a single achievement dictionary into a readable Discord message string.
def format_achievement(ach):
    player = f"**{ach['player']['displayName']}**"
    metric = ach.get("metric", "")
    atype = ach.get("type", "").lower()
    name = ach.get("name", "")
    metric_clean = metric.replace("_", " ").replace("-", " ").title()

    try:
        value = name.replace(metric_clean, "").strip()
    except Exception:
        value = ""

    if metric in SKILLS and atype == "level":
        return f"{player} has achieved level {value} {metric_clean}!"

    if metric in SKILLS and atype == "experience":
        return f"{player} has achieved {value} {metric_clean} experience!"

    if metric == "overall":
        return f"{player} has achieved {value} total XP!"

    if metric in CLUES:
        clue_type = CLUES[metric]
        return f"{player} has achieved {value} {clue_type} clue completions!"

    if metric in BOSSES:
        return f"{player} has achieved {value} {metric_clean} kills!"

    if metric in {'base_stats', 'combat_level'}:
        return f"{player} has achieved base {value} stats!"

    if metric in ACTIVITIES:
        return f"{player} has achieved {value} {metric_clean}!"

    return f"{player} has achieved {value} {metric_clean}!"

#Sends a batch of achievements to the set Discord webhook.
def send_to_discord(achievements):
    if not achievements:
        return

    header = get_daily_header() #Get date + random headline.
    lines = [f"{format_achievement(a)}" for a in achievements]
    summary = "\n".join([header] + lines)

    print("Sending batch message to Discord:")
    print(summary)

    requests.post(DISCORD_WEBHOOK_URL, json={"content": summary})

#Load the timestamp of the most recent achievement we've already posted.
def load_last_seen():
    try:
        with open("last_achievement.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        #Fallback if the file doesn't exist yet.
        return "2000-01-01T00:00:00.000Z"

#Save the most recent achievement timestamp so it doesn't get repeated tomorrow.
def save_last_seen(latest_timestamp):
    with open("last_achievement.json", "w") as f:
        json.dump(latest_timestamp, f)

#Pull the full list of recent achievements from the Wise Old Man API.
def fetch_achievements():
    url = "https://api.wiseoldman.net/v2/groups/976/achievements"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

#Main execution function for the daily update cycle.
def main():
    print("Waiting 5 minutes before checking for new achievements...")
    time.sleep(5 * 60) #Wait to give WOM backend time to process player updates so we actually get new achievements. 5 minutes might be too little depending on clan size idk.

    print("Fetching latest achievements...")
    achievements = fetch_achievements()
    last_seen = load_last_seen()

    #Filter only the new achievements (after last seen).
    new_achievements = [a for a in achievements if a["createdAt"] > last_seen]

    if new_achievements:
        new_achievements.reverse() #Ensure oldest-to-newest order
        send_to_discord(new_achievements)
        save_last_seen(new_achievements[-1]["createdAt"])
    else:
        print("No new achievements found.")

#Run main only if script is executed directly (not imported)
if __name__ == "__main__":
    main()
