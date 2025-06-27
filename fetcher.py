import requests

url = "https://api.wiseoldman.net/v2/groups/976/achievements"
achievements = requests.get(url).json()

if achievements:
    print("Most recent timestamp:", achievements[0]["createdAt"])
else:
    print("No achievements found.")
