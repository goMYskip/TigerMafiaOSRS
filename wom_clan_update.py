import requests
import os

#Group ID of the MudSk1pperz clan on wiseoldman.net
GROUP_ID = 976

#The private group verification code is loaded from an environment variable.
#It is stored as a secret named WOM_VERIFICATION_CODE.
VERIFICATION_CODE = os.environ.get("WOM_VERIFICATION_CODE")

#Construct the API URL for updating the group.
API_URL = f"https://api.wiseoldman.net/v2/groups/{GROUP_ID}/update-all"

#Prepare the request payload with the required verification code.
payload = {
    "verificationCode": VERIFICATION_CODE
}

#Sends a POST request to Wise Old Man API to update the group's member data.
def update_group():
    response = requests.post(API_URL, json=payload)
    try:
        data = response.json() #Attempt to parse the JSON response.
    except:
        data = response.text #Fallback to raw text if JSON decoding fails

    if response.status_code == 200:
        print("Group update request accepted.")
        print("Response:", data)
    else:
        print(f"Failed to update group. Status: {response.status_code}")
        print("Response:", data)

#Run the update when the script is executed
update_group()
