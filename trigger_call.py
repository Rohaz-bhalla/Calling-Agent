import requests
import os
from dotenv import load_dotenv

load_dotenv()

# FIX 1: The correct endpoint is singular "/call"
url = "https://api.videosdk.live/v2/sip/call"

headers = {
    "Authorization": os.getenv("VIDEOSDK_AUTH_TOKEN"),
    "Content-Type": "application/json"
}

payload = {
    "gatewayId": "b9cee9d9-97bf-4ca3-a6da-ce0366ecb88a", 
    
    # FIX 2: VideoSDK requires this exact parameter name
    "sipCallTo": "+916283583232", 
    
    # FIX 3: VideoSDK requires this exact parameter name
    "destinationRoomId": "qgmu-hvns-4xcp" 
}

try:
    print(f"Dialing {payload['sipCallTo']}...")
    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status() 
    
    print("\n✅ Call triggered successfully! Your phone should be ringing.")
    print(response.json())
    
except requests.exceptions.RequestException as e:
    print("\n❌ Failed to trigger call.")
    print(f"Error: {e}")
    if 'response' in locals() and response.text:
        print(f"API Details: {response.text}")