# ---------------------------- IMPORTS ------------------------------- #
# Allows you to read the .env file
from dotenv import load_dotenv
import os
# variable = os.getenv("<ENV VARIABLE>")
import requests
# ---------------------------- CONSTANTS ------------------------------- #

# ---------------------------- GLOBAL VARIABLES ------------------------------- #

# ---------------------------- FUNCTIONS ------------------------------- #

# ---------------------------- UI SETUP ------------------------------- #

# Handles most of the response errors in the code basic API call not Async
try:
    response = requests.get("http://api.open-notify.org/iss-now.json")
    iss_location_data = response.json()
    print(response.json())
    iss_coordinates = (iss_location_data["iss_position"]["longitude"], iss_location_data["iss_position"]["latitude"])
    print(iss_coordinates)
except requests.exceptions.HTTPError as http_err:
    print(f"HTTP error: {http_err}")  # Catches 4xx/5xx
except requests.exceptions.RequestException as err:
    print(f"Error: {err}")  # Catches connectivity/other issues
finally:
    print("API request attempt complete.")
