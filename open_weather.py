# ---------------------------- IMPORTS ------------------------------- #
# Allows you to read the .env file
from dotenv import load_dotenv
import os
# Async API Python calls
import asyncio
import httpx
import datetime as dt
# ---------------------------- CONSTANTS ------------------------------- #
load_dotenv()
IP_LOCATION_API_ENDPOINT= os.getenv("IP_LOCATION_API_ENDPOINT")
OPEN_WEATHER_API_KEY= os.getenv("OPEN_WEATHER_API_KEY")
OPEN_WEATHER_API_ENDPOINT= os.getenv("OPEN_WEATHER_API_ENDPOINT")
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
print(current_weather_data)