# ---------------------------- IMPORTS ------------------------------- #
# Allows you to read the .env file
from dotenv import load_dotenv
import os
import asyncio
import httpx
import datetime as dt
# ---------------------------- CONSTANTS ------------------------------- #
load_dotenv()
SUNRISE_SUNSET_API_ENDPOINT = os.getenv("SUNRISE_SUNSET_API_ENDPOINT")
IP_LOCATION_API_ENDPOINT = os.getenv("IP_LOCATION_API_ENDPOINT")
ISS_LOCATION_API_ENDPOINT = os.getenv("ISS_LOCATION_API_ENDPOINT")
# ---------------------------- GLOBAL VARIABLES ------------------------------- #
# Retrieve date and prepare format for other API call
today = dt.datetime.today().strftime("%Y-%m-%d")
# ---------------------------- FUNCTIONS ------------------------------- #
async def fetch_data(url):
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        return response.json()

async def main():
    # Use this if you need all the data at once
    # ____________________________________________________________
    # urls = [IP_LOCATION_API_ENDPOINT, ISS_LOCATION_API_ENDPOINT]
    # tasks = [fetch_data(url) for url in urls]
    # results = await asyncio.gather(*tasks)
    # print(results)
    # ____________________________________________________________
    # Retrieve current position API request using Async to feed one api into another
    current_location_results = await asyncio.gather(
        fetch_data(IP_LOCATION_API_ENDPOINT),
    )
    # print(current_location_results)
    # print(current_location_results[0]["loc"])
    # print(type(current_location_results[0]["loc"]))
    current_latitude, current_longitude = current_location_results[0]["loc"].split(",")
    current_timezone = current_location_results[0]["timezone"]
    # print(current_latitude)
    # print(current_longitude)
    # print(current_timezone)
    # Retrieve current sunset/sunrise API request using results from first api request
    sunrise_sunset_api_endpoint_with_params = f"{SUNRISE_SUNSET_API_ENDPOINT}lat={current_latitude}&lng={current_longitude}&date={today}&tzid={current_timezone}"
    current_sunrise_sunset_results = await asyncio.gather(
        fetch_data(sunrise_sunset_api_endpoint_with_params),
    )
    return current_sunrise_sunset_results, current_location_results

# ---------------------------- UI SETUP ------------------------------- #
current_sunrise_sunset_results, current_location_results = asyncio.run(main())
current_city = current_location_results[0]["city"]
current_sunrise_time = current_sunrise_sunset_results[0]["results"]["sunrise"]
current_sunset_time = current_sunrise_sunset_results[0]["results"]["sunset"]

print("Current City: ", current_city)
print("Current Sunrise Time: ", current_sunrise_time)
print("Current Sunset Time: ", current_sunset_time)
