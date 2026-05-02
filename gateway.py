import requests
from dotenv import load_dotenv
import os

load_dotenv()

# 1. Define the API endpoint
url = "https://api.videosdk.live/v2/sip/outbound-gateways"

# 2. Set up your headers (Make sure to paste your actual token here)
headers = {
    "Authorization": os.getenv("VIDEOSDK_AUTH_TOKEN"),
    "Content-Type": "application/json"
}

# 3. Define the payload using the exact detail
payload = {
    "name": "Twilio-Rohaz",
    "numbers": ["+15074076909"],
    "address": "rohazbhallavideosdk.pstn.twilio.com", # Added 'sip:' as the standard protocol prefix
    "transport": "udp",
    "auth": {
        "username": os.getenv("PAYLOAD_ID"),
        "password": os.getenv("PAYLOAD_PASSWORD")
    }
}

# 4. Make the POST request to create the gateway
try:
    print("Sending request to VideoSDK...")
    response = requests.post(url, json=payload, headers=headers)
    
    # Check if the request was successful
    response.raise_for_status() 
    
    print("\n✅ Gateway Created Successfully!")
    print(response.json())
    
except requests.exceptions.RequestException as e:
    print("\n❌ Failed to create gateway.")
    print(f"Error: {e}")
    # If the API sends back a specific reason (like an invalid token or bad address format), this will print it:
    if response.text:
        print(f"API Details: {response.text}")