import requests
import os

url = os.environ.get("DISCORD_WEBHOOK_URL")
print(f"Webhook URL: {url}")  # <-- Debug print

if not url:
    print("❌ DISCORD_WEBHOOK_URL is not set.")
else:
    response = requests.post(url, json={"content": "🏅 **TestPlayer** achieved **99 Magic** on 2025-06-26!"})
    print(f"✅ Sent! Status: {response.status_code}")
    print("Response:", response.text)
