import time
import json
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import urllib.parse

# OAuth details
CLIENT_ID = "46899977096215655"
CLIENT_SECRET = "9d85c43b1482497dbbce61f6e4aa173a433796eeae2ca8c5f6129f2dc4de46d9"
REDIRECT_URI = "https://embed.gog.com/on_login_success?origin=client"

# Step 1: Start Selenium and open the GOG login page
auth_url = f"https://auth.gog.com/auth?client_id={CLIENT_ID}&redirect_uri={urllib.parse.quote(REDIRECT_URI)}&response_type=code&layout=client2"
options = webdriver.ChromeOptions()
options.headless = False
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
print("Opening browser for GOG login...")
driver.get(auth_url)

# Step 2: Wait for the user to log in manually (this assumes user is logged in on GOG)
input("Please log in to GOG, then press Enter once you're logged in and redirected...")

# Step 3: Grab the authorization code from the redirected URL
current_url = driver.current_url
print(f"Redirected URL: {current_url}")

# Parse the URL to get the authorization code
parsed_url = urllib.parse.urlparse(current_url)
query_params = urllib.parse.parse_qs(parsed_url.query)
authorization_code = query_params.get('code', [None])[0]
if not authorization_code:
    print("Error: Unable to find the authorization code in the redirected URL.")
    driver.quit()
    exit()
print(f"Authorization Code: {authorization_code}")

# Step 4: Exchange the authorization code for the access token
token_url = f"https://auth.gog.com/token?client_id={CLIENT_ID}&client_secret={CLIENT_SECRET}&grant_type=authorization_code&code={authorization_code}&redirect_uri={urllib.parse.quote(REDIRECT_URI)}"
response = requests.get(token_url)
if response.status_code == 200:
    token_data = response.json()
    print("Authentication successful!")

    # Prepare the data in the desired format
    auth_data = {
        CLIENT_ID: {
            "access_token": token_data['access_token'],
            "expires_in": token_data['expires_in'],
            "token_type": token_data['token_type'],
            "scope": token_data.get('scope', ''),
            "session_id": token_data['session_id'],
            "refresh_token": token_data['refresh_token'],
            "user_id": token_data['user_id'],
            "loginTime": time.time()
        }
    }

    # Step 5: Save the data to auth.json
    with open("auth.json", "w") as f:
        json.dump(auth_data, f, indent=4)
    print(f"Access token and refresh token saved to auth.json.")
else:
    print(f"Error: Unable to retrieve access token. Status code: {response.status_code}")
    print(response.text)

# Close the browser
driver.quit()
