import requests
import os

#This script is a simple test utility for verifying that your Discord webhook is working correctly. 
#It assumes a secret variable saved in your github repo. It sends a sample message to the webhook URL stored in the DISCORD_WEBHOOK_URL environment variable.

#Retrieve the webhook URL from environment variables.
url = os.environ.get("DISCORD_WEBHOOK_URL")
print(f"Webhook URL: {url}")

#If the URL is not set, warn the user.
if not url:
    print("DISCORD_WEBHOOK_URL is not set.")
else:
    #Send a test message to the webhook.
    response = requests.post(url, json={"content": "**TestPlayer** achieved **99 Magic**"})

    #Print the HTTP response status and content for debugging
    print(f"Sent! Status: {response.status_code}")
    print("Response:", response.text)
