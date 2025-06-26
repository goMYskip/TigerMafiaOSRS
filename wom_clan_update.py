import requests
import os

GROUP_ID = 976
VERIFICATION_CODE = os.environ.get("WOM_VERIFICATION_CODE")  # Read from GitHub Actions secret
API_URL = f"https://api.wiseoldman.net/v2/groups/{GROUP_ID}/update-all"

payload = {
    "verificationCode": VERIFICATION_CODE
}

def update_group():
    response = requests.post(API_URL, json=payload)
    try:
        data = response.json()
    except:
        data = response.text

    if response.status_code == 200:
        print("✅ Group update request accepted.")
        print("📦 Response:", data)
    else:
        print(f"❌ Failed to update group. Status: {response.status_code}")
        print("📦 Response:", data)

update_group()
