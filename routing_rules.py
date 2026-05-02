import requests
import os
from dotenv import load_dotenv

# 1. Load variables from the .env file into the environment
load_dotenv()

# 2. Define the API endpoint
url = "https://api.videosdk.live/v2/sip/routing-rules"

# 3. Set up headers (os.getenv will now pull seamlessly from your .env file)
headers = {
    "Authorization": os.getenv("VIDEOSDK_AUTH_TOKEN"),
    "Content-Type": "application/json"
}

# 4. Define the payload for the rule
payload = {
    "name": "MyTelephonyAgent",
    "gatewayId": "8f84f21f-024a-4eab-b7d3-fc6c016b67f6",
    "numbers": ["+15074076909"] 
}

# 5. Make the POST request
try:
    print("Sending routing rule request to VideoSDK...")
    response = requests.post(url, json=payload, headers=headers)
    
    response.raise_for_status() 
    
    print("\n✅ Routing Rule Created Successfully!")
    print(response.json())
    
except requests.exceptions.RequestException as e:
    print("\n❌ Failed to create routing rule.")
    print(f"Error: {e}")
    if response.text:
        print(f"API Details: {response.text}")