import requests

#This script fetches the most recent achievement data from your clan (MudSk1pperz in my case), using the Wise Old Man API.

#Links to the clan's achievements
url = "https://api.wiseoldman.net/v2/groups/976/achievements"

#Sends GET request to the WOM API
achievements = requests.get(url).json()

#If any new achievements are returned, print the timestamp of the newest one
if achievements:
    print("Most recent timestamp:", achievements[0]["createdAt"])
else:
    print("No achievements found.")
