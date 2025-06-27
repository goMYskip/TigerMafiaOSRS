import os
import json
import time
import requests

DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")

SKILLS = ['attack', 'defence', 'strength', 'hitpoints', 'ranged', 'prayer', 'magic', 'cooking', 'woodcutting', 'fletching', 'fishing', 'firemaking', 'crafting', 'smithing', 'mining', 'herblore', 'agility', 'thieving', 'slayer', 'farming', 'runecrafting', 'hunter', 'construction']
BOSSES = {'abyssal-sire', 'mimic', 'tzkal-zuk', 'giant-mole', 'theatre-of-blood-hard-mode', 'venenatis', 'hespori', 'kalphite-queen', 'grotesque-guardians', 'phosanis-nightmare', 'sarachnis', 'the-gauntlet', 'the-corrupted-gauntlet', 'kraken', 'barrows-chests', 'dagannoth-supreme', 'skotizo', 'scorpia', 'callisto', 'crazy-archaeologist', 'king-black-dragon', 'tempoross', 'alchemical-hydra', 'theatre-of-blood', 'vorkath', 'general-graardor', 'chambers-of-xeric', 'bryophyta', 'commander-zilyana', 'dagannoth-rex', 'obor', 'wintertodt', 'dagannoth-prime', 'chambers-of-xeric-challenge-mode', 'kril-tsutsaroth', 'tztok-jad', 'corporeal-beast', 'vetion', 'zulrah', 'nex', 'kree-ara', 'deranged-archaeologist', 'thermonuclear-smoke-devil', 'chaos-elemental', 'nightmare', 'zalcano', 'cerberus', 'chaos-fanatic'}
CLUES = {'clue_scroll_all': 'All', 'clue_scroll_beginner': 'Beginner', 'clue_scroll_easy': 'Easy', 'clue_scroll_medium': 'Medium', 'clue_scroll_hard': 'Hard', 'clue_scroll_elite': 'Elite', 'clue_scroll_master': 'Master'}
ACTIVITIES = ['last-man-standing', 'pvp-arena', 'soul-wars-zeal', 'guardian-defence', 'rifts-closed']

def format_achievement(ach):
    player = ach["player"]["displayName"]
    metric = ach.get("metric", "")
    atype = ach.get("type", "").lower()

    metric_clean = metric.replace("_", " ").replace("-", " ").title()

    if metric in SKILLS and atype.isdigit():
        return f"{player} has achieved level {atype} {metric.title()}!"

    if metric in SKILLS and atype.endswith("m"):
        return f"{player} has achieved {atype} {metric.title()} experience!"

    if metric == "overall":
        return f"{player} has achieved {atype} total XP!"

    if metric in CLUES:
        clue_type = CLUES[metric]
        return f"{player} has achieved {atype} {clue_type} clue completions!"

    if metric in BOSSES:
        return f"{player} has achieved {atype} {metric_clean} kills!"

    if metric in {'base_stats', 'combat_level'}:
        return f"{player} has achieved base {atype} stats!"

    if metric in ACTIVITIES:
        return f"{player} has achieved {atype} {metric_clean}!"

    return f"{player} has achieved {atype} {metric_clean}!"

def send_to_discord(achievements):
    for ach in achievements:
        msg = format_achievement(ach)
        print("Sending:", msg)
        requests.post(DISCORD_WEBHOOK_URL, json={"content": f"{msg}"})

def load_last_seen():
    try:
        with open("last_achievement.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return "2000-01-01T00:00:00.000Z"

def save_last_seen(latest_timestamp):
    with open("last_achievement.json", "w") as f:
        json.dump(latest_timestamp, f)

def fetch_achievements():
    url = "https://api.wiseoldman.net/v2/groups/976/achievements"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

def main():
    print("Waiting 5 minutes before checking for new achievements...")
    time.sleep(5 * 60)

    print("Fetching latest achievements...")
    achievements = fetch_achievements()
    last_seen = load_last_seen()

    new_achievements = [a for a in achievements if a["createdAt"] > last_seen]

    if new_achievements:
        new_achievements.reverse()
        send_to_discord(new_achievements)
        save_last_seen(new_achievements[-1]["createdAt"])
    else:
        print("No new achievements found.")

if __name__ == "__main__":
    main()
