import praw
from constants import CLIENT_ID, CLIENT_SECRET, USER_AGENT, USERNAME, PASSWORD

import requests
from requests.auth import HTTPBasicAuth

# Reddit app credentials
CLIENT_ID = CLIENT_ID
CLIENT_SECRET = CLIENT_SECRET
REDIRECT_URI = "http://localhost:8080"
USER_AGENT = USER_AGENT
auth_code = 'JthTpL0mqgg6NFzWUHSK-OHnQBtMYA'


# Step 1: Get access token
auth = HTTPBasicAuth(CLIENT_ID, CLIENT_SECRET)
data = {
    'grant_type': 'password',
    'username': USERNAME,
    'password': PASSWORD
}
headers = {'User-Agent': USER_AGENT}

response = requests.post("https://www.reddit.com/api/v1/access_token",
                         auth=auth, data=data, headers=headers)

if response.status_code == 200:
    token = response.json()['access_token']
    print(f"Access Token: {token}")
else:
    print(f"Error: {response.status_code} - {response.text}")