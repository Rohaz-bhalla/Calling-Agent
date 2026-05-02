import requests

# 🚨 PASTE YOUR TOKEN DIRECTLY HERE (Make sure it starts with 'eyJ'!)
TOKEN = "YOUR_MASSIVE_TOKEN_HERE"

url = "https://api.videosdk.live/v2/rooms"
headers = {
    "Authorization": TOKEN,
    "Content-Type": "application/json"
}

try:
    print(f"Testing with Token starting with: {TOKEN[:10]}...")
    response = requests.post(url, headers=headers)
    response.raise_for_status() 
    
    room_data = response.json()
    room_id = room_data.get('roomId')
    
    print(f"\n✅ IT FINALLY WORKED!")
    print(f"👉 YOUR ROOM ID: {room_id} 👈")
    
except requests.exceptions.RequestException as e:
    print("\n❌ Still failing.")
    print(f"Error: {e}")
    if response.text:
        print(f"API Details: {response.text}")