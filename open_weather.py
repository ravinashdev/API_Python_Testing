# ---------------------------- IMPORTS ------------------------------- #
# Allows you to read the .env file
from pyexpat.errors import messages

from dotenv import load_dotenv
import os
# Twillio
from twilio.rest import Client
# Async API Python calls
import asyncio
import httpx
# ---------------------------- CONSTANTS ------------------------------- #
load_dotenv()
IP_LOCATION_API_ENDPOINT= os.getenv("IP_LOCATION_API_ENDPOINT")
OPEN_WEATHER_API_KEY= os.getenv("OPEN_WEATHER_API_KEY")
OPEN_WEATHER_API_ENDPOINT= os.getenv("OPEN_WEATHER_API_ENDPOINT")
TWILLIO_TEST_ACCOUNT_SID= os.getenv("TWILLIO_TEST_ACCOUNT_SID")
TWILLIO_TEST_AUTH_TOKEN= os.getenv("TWILLIO_TEST_AUTH_TOKEN")

# ---------------------------- GLOBAL VARIABLES ------------------------------- #


# ---------------------------- FUNCTIONS ------------------------------- #
async def fetch_data(url, params):
    async with httpx.AsyncClient() as client:
        response = await client.get(url=url, params=params)
        return response.json()
async def main():
    try:
        current_location_results = await asyncio.gather(
            fetch_data(IP_LOCATION_API_ENDPOINT, params={}),
        )
        current_latitude, current_longitude = current_location_results[0]["loc"].split(",")
        current_city = current_location_results[0]["city"]
        # Open weather API params
        params = {
            "q": current_city,
            "APPID": OPEN_WEATHER_API_KEY,
        }
        current_weather_results = await asyncio.gather(
            fetch_data(OPEN_WEATHER_API_ENDPOINT, params=params)
        )
    except Exception as e:
        print(e)
    return current_weather_results

# ---------------------------- UI SETUP ------------------------------- #
current_weather_data = asyncio.run(main())
current_city = current_weather_data[0]["name"]
current_description = current_weather_data[0]["weather"][0]["description"]
message=f"Weather Update: There are some {current_description} in {current_city} right now"

# Twillio SMS Test
client = Client(TWILLIO_TEST_ACCOUNT_SID, TWILLIO_TEST_AUTH_TOKEN)
message = client.messages.create(
    body=message,
    from_="+18559411028",
    to="+13478579787",
)