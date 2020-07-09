#!/usr/bin/python

import datetime
import os
import sys
import time
import json
import requests
import random
from station import Station

MEASUREMENT_INTERVAL = 10  # minutes
WEATHER_UPLOAD = False
WU_URL = "http://weatherstation.wunderground.com/weatherstation/updateweatherstation.php"

' support for python2 and python3 '
try:
    from urllib import urlencode
except ImportError:
    from urllib.parse import urlencode

try:
    import urllib.request as urllib2
except ImportError:
    import urllib2

try:
    from sense_hat import SenseHat
except ImportError:
    print("SenseHat module not found.")

def exec_test():
    print("Initializing test station...")
    test_station = Station("Main Station","KTXFORTW595","wheaxkqp")
    # run test with sample values
    while True:
        sample_weather_data = {
            "dateutc": "now",
            "tempf": str(random.randint(32, 110)),
            "humidity": str(random.randint(40, 99)),
            "baromin": str(random.randint(1, 99)),
        }

        test_station.broadcast_info(sample_weather_data)
        time.sleep(5)   # sleep for 5 second intervals

def check_parameters(parameter):
    # none or -t for testing
    valid_parameters = ["-t", ""]

    if parameter not in valid_parameters:
        return False

    return True    

############
#   MAIN   #
############
def main():
    exec_test()

if __name__ == "__main__":
    program_name = sys.argv[0]
    parameter = sys.argv[1]
    if check_parameters(parameter) :
        print("Invalid Usage! \nUsage: python weather_station.py params: [-t]")
        print("Given: " + program_name + " " + parameter)
        sys.exit(-1)
    else:
        print("Startup: " + program_name + " " + parameter )
        if parameter == "-t":
            exec_test()
        else:
            try:
                main()
            except KeyboardInterrupt:
                print("\nExiting application\n")
                sys.exit(0)
