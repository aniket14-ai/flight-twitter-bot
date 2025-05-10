import os
import requests
import tweepy
from dotenv import load_dotenv

load_dotenv()

# Twitter credentials from .env
API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
ACCESS_SECRET = os.getenv("ACCESS_SECRET")

# Set up Tweepy client
auth = tweepy.OAuth1UserHandler(API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_SECRET)
api = tweepy.API(auth)

# OpenSky API call
def get_flight_info(target_flight="6E203"):
    url = "https://opensky-network.org/api/states/all"
    try:
        res = requests.get(url, timeout=10)
        data = res.json()
        for flight in data.get("states", []):
            callsign = flight[1].strip() if flight[1] else ""
            if callsign == target_flight:
                lat = flight[6]
                lon = flight[5]
                alt = int(flight[7]) if flight[7] else 0
                return f"✈️ Flight {callsign} is airborne!\n🛰️ Altitude: {alt}m\n🌍 Location: lat {lat}, lon {lon}"
        return f"⚠️ Flight {target_flight} not found in the air."
    except Exception as e:
        return f"🚨 Error fetching flight: {str(e)}"

# Run and tweet
flight_info = get_flight_info("6E203")
api.update_status(flight_info)
print("Tweeted:", flight_info)
