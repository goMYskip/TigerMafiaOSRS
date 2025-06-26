import requests
import os

url = os.environ.get("DISCORD_WEBHOOK_URL")
requests.post(url, json={"content": "🏅 **TestPlayer** achieved **99 Magic** on 2025-06-26!"})
