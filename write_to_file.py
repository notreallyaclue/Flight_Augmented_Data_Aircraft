# Queries the API and Writes to file
# Theres is a time.sleep to avoid the server being bombarded, Please respect that
# the server only updates every half a second anyway

import requests
import json
import time

while True:
    # The Url composes of a few specifiers.
    # lat=00.00000&lng=00.00000  Need to be your coordinates, get them from google maps.
    # fDstL=0 <This is the minimum distnace to search for aircraft. fDstU=10  < this is the maximum distance (Km) from your location to search
    # for aircraft.
    # fAltL=0 and fAltU=5000 is minimum and maximum altitude to search for aircraft (feet)

    url = 'https://public-api.adsbexchange.com/VirtualRadar/AircraftList.json?lat=00.000000&lng=00.000000&fDstL=0&fDstU=100&fAltL=0&fAltU=5000'
    resp_dict = requests.get(url)
    resp_dict = json.loads(resp_dict.content)
    aircraft = resp_dict['acList']

    if len(aircraft) >= 1:  # if there is information in the list
        aircraft = aircraft[0]
        Call = str(aircraft.get("Call", None))
        Alt = str(aircraft.get("Alt", None))
        Spd = str(aircraft.get("Spd", None))
        Op = str(aircraft.get("Op", None))
        Mdl = str(aircraft.get("Mdl", None))
        Lat = str(aircraft.get("Lat", None))
        Long = str(aircraft.get("Long", None))
    else:
        Call = 'None'
        Alt = 'None'
        Spd = 'None'
        Op = 'None'
        Mdl = 'None'
        Lat = 'None'
        Long = 'None'

    f = open('filename.txt', 'w')
    f.write(Call + '\n')
    f.write(Alt + '\n')
    f.write(Spd + '\n')
    f.write(Op + '\n')
    f.write(Mdl + '\n')
    f.write(Lat + '\n')
    f.write(Long + '\n')
    f.close()

    time.sleep(0.5)
