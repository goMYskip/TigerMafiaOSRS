import datetime
import json
import random
from pathlib import Path

HEADLINES = [
    "Of course the bloody incredible MudSk1p squad once again has done something truly remarkable.",
    "We have some :bangbang:BREAKING NEWS:bangbang: over at the MudSkip clan:",
    ":dogwater:***Woof Woof!***:Dog:—wait, is that a dog? Is that Mayh? Wait, no! it is the Mudsk1pperz barking up a storm once again!",
    "Ouughhehhhn",
    "Wagwan fam, news innit?",
    "Reporters say this is something never seen before. Something no one has ever done before. This might genuinely be a world first.",
    "Hey guys could we not schedule officials for 20? I have to eat dinner with my family.",
    ":bangbang:A NUCLEAR STRIKE HEADING STRAIGHT FOR HULL HAS BEEN DETECTED:bangbang: \"Good riddance.\" - Keir Starmer",
    "The announcement today might not be a new logjam update, but it is the next best thing. Mud Skip News.",
    "I'm never letting Figaro write a news headline again the burtons on my keybaort is all fuicking chewed on.",
    "GZZZZ",
    "You know they actually keep me locked in a dark and damp room in Darkmeyer and have me write these, right? By contributing to these news, you are contributing to my suffering.",
    "A Saradoming brew and a Super restore, just 10,000 GP today at Tesco's meal deal.",
    "Tragically, with today's game update you will be able to buy XP lamps through the new Squeal of Fortune. LOL u got pranked here is actually the crazy news of the day."
]

USED_HEADLINES_PATH = "used_headlines.json"

def get_daily_header():
    # Load used headlines
    try:
        with open(USED_HEADLINES_PATH, "r") as f:
            used = json.load(f)
    except FileNotFoundError:
        used = []

    available = [h for h in HEADLINES if h not in used]

    if not available:
        used = []
        available = HEADLINES[:]

    chosen = random.choice(available)
    used.append(chosen)

    with open(USED_HEADLINES_PATH, "w") as f:
        json.dump(used, f)

    # Format date
    today = datetime.date.today()
    day = today.day
    suffix = "th" if 11 <= day <= 13 else {1: "st", 2: "nd", 3: "rd"}.get(day % 10, "th")
    date_str = f"**{day}{suffix} of {today.strftime('%B')}**"

    return f"{date_str}\n{chosen}"
