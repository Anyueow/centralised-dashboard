from src.reddit.collection import red

# Use the code from the URL to authorize the application
auth_code = 'JthTpL0mqgg6NFzWUHSK-OHnQBtMYA'

# Authorize using the code
red.auth.authorize(auth_code)

# Test connection
# Authorize using the code
try:
    refresh_token = red.auth.authorize(auth_code)
    print(f"Logged in as: {red.user.me()}")
    print(f"Refresh Token: {refresh_token}")
except Exception as e:
    print(f"Authentication failed: {e}")