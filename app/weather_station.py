#!/usr/bin/python

import datetime
import os
import sys
import time
import json
import requests
import random
from station import *
from config import Config

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
    test_station = Station()
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

def main():
    global last_temp
    weather_data = {}
    # initialize the lastMinute variable to the current time to start
    last_minute = datetime.datetime.now().minute
    # on startup, just use the previous minute as lastMinute
    last_minute -= 1
    if last_minute == 0:
        last_minute = 59

    # infinite loop to continuously check weather values
    while 1:
        # The temp measurement smoothing algorithm's accuracy is based
        # on frequent measurements, so we'll take measurements every 5 seconds
        # but only upload on measurement_interval
        current_second = datetime.datetime.now().second
        # are we at the top of the minute or at a 5 second interval?
        if (current_second == 0) or ((current_second % 5) == 0):
            # ========================================================
            # read values from the Sense HAT
            # ========================================================
            # Calculate the temperature. The get_temp function 'adjusts' the recorded temperature adjusted for the
            # current processor temp in order to accommodate any temperature leakage from the processor to
            # the Sense HAT's sensor. This happens when the Sense HAT is mounted on the Pi in a case.
            # If you've mounted the Sense HAT outside of the Raspberry Pi case, then you don't need that
            # calculation. So, when the Sense HAT is external, replace the following line (comment it out  with a #)
            calc_temp = get_temp()
            # with the following line (uncomment it, remove the # at the line start)
            # calc_temp = sense.get_temperature_from_pressure()
            # or the following line (each will work)
            # calc_temp = sense.get_temperature_from_humidity()
            # ========================================================
            # At this point, we should have an accurate temperature, so lets use the recorded (or calculated)
            # temp for our purposes
            temp_c = round(calc_temp, 1)
            temp_f = round(c_to_f(calc_temp), 1)
            humidity = round(sense.get_humidity(), 0)
            # convert pressure from millibars to inHg before posting
            pressure = round(sense.get_pressure() * 0.0295300, 1)
            print("Temp: %sF (%sC), Pressure: %s inHg, Humidity: %s%%" % (temp_f, temp_c, pressure, humidity))
            weather_data = {
                "action": "updateraw",
                "ID": wu_station_id,
                "PASSWORD": wu_station_key,
                "dateutc": "now",
                "tempf": str(temp_f),
                "humidity": str(humidity),
                "baromin": str(pressure),
            }
            user_data = {
                "tempf": str(temp_f),
                "humidity": str(humidity),
                "baromin": str(pressure),
            }
            broadcast_info(user_data)
            # get the current minute
            current_minute = datetime.datetime.now().minute
            # is it the same minute as the last time we checked?
            if current_minute != last_minute:
                # reset last_minute to the current_minute
                last_minute = current_minute
                # is minute zero, or divisible by 10?
                # we're only going to take measurements every MEASUREMENT_INTERVAL minutes
                if (current_minute == 0) or ((current_minute % MEASUREMENT_INTERVAL) == 0):
                    # get the reading timestamp
                    now = datetime.datetime.now()
                    print("\n%d minute mark (%d @ %s)" % (MEASUREMENT_INTERVAL, current_minute, str(now)))
                    # did the temperature go up or down?
                    if last_temp != temp_f:
                        if last_temp > temp_f:
                            # display a blue, down arrow
                            sense.set_pixels(arrow_down)
                        else:
                            # display a red, up arrow
                            sense.set_pixels(arrow_up)
                    else:
                        # temperature stayed the same
                        # display red and blue bars
                        sense.set_pixels(bars)
                    # set last_temp to the current temperature before we measure again
                    last_temp = temp_f

                    # is weather upload enabled (True)?
                    if WEATHER_UPLOAD:
                        # From http://wiki.wunderground.com/index.php/PWS_-_Upload_Protocol
                        print("Uploading data to Weather Underground")
                        # build a weather data object
                        weather_data = {
                            "action": "updateraw",
                            "ID": wu_station_id,
                            "PASSWORD": wu_station_key,
                            "dateutc": "now",
                            "tempf": str(temp_f),
                            "humidity": str(humidity),
                            "baromin": str(pressure),
                        }
                        try:
                            upload_url = WU_URL + "?" + urlencode(weather_data)
                            response = urllib2.urlopen(upload_url)
                            html = response.read()
                            print("Server response:", html)
                            # do something
                            response.close()  # best practice to close the file
                        except:
                            print("Exception:", sys.exc_info()[0], SLASH_N)
                    else:
                        print("Skipping Weather Underground upload")

        time.sleep(1)  # this should never happen since the above is an infinite loop

if (MEASUREMENT_INTERVAL is None) or (MEASUREMENT_INTERVAL > 60):
    print("The application's 'MEASUREMENT_INTERVAL' cannot be empty or greater than 60")
    sys.exit(1)

############
#   MAIN   #
############
if __name__ == "__main__":
    program_name = sys.argv[0]
    parameter = sys.argv[1]
    if parameter == None or parameter != "-t":
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
