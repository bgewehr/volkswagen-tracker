import requests
from time import sleep
from database.influx import add_entry

from vw_carnet import CarNetLogin, getMileage, getRange
from environment import get_username, get_password, get_update_interval


# Login information for the VW CarNet app
CARNET_USERNAME = get_username()  # Insert your credentials here, if you run this application manually
CARNET_PASSWORD = get_password()  # Insert your credentials here, if you run this application manually

s = requests.Session()  # Create a session to save cookies and connection data
url = CarNetLogin(s, CARNET_USERNAME, CARNET_PASSWORD)  # Login and receive the custom URL for your Carnet account
# the authentication information doesn't get refreshed once the container started, this might be a problem later...

"""Request data every X hours and write it to the database"""
while True:
    distanceCovered_str = getMileage(s, url)  # Pull the information from Carnet
    distanceCovered = int(distanceCovered_str.replace(".", ""))
    current_range = int(getRange(s, url))
    add_entry(distanceCovered, current_range)  # Insert the value into the database
    sleep(1 * 60 * 60 * get_update_interval())  # Wait for X h
