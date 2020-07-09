import datetime
import os
import sys
import time
import json
import requests
import random
from sense_hat import SenseHat 

MEASUREMENT_INTERVAL = 10  # minutes
WEATHER_UPLOAD = False
WU_URL = "http://weatherstation.wunderground.com/weatherstation/updateweatherstation.php"
SINGLE_HASH = "#"
HASHES = "########################################"
SLASH_N = "\n"
SERVER_URL = "http://192.168.1.9:8080/update"

b = [0, 0, 255]  # blue
r = [255, 0, 0]  # red
e = [0, 0, 0]  # empty
# create images for up and down arrows
arrow_up = [
    e, e, e, r, r, e, e, e,
    e, e, r, r, r, r, e, e,
    e, r, e, r, r, e, r, e,
    r, e, e, r, r, e, e, r,
    e, e, e, r, r, e, e, e,
    e, e, e, r, r, e, e, e,
    e, e, e, r, r, e, e, e,
    e, e, e, r, r, e, e, e
]
arrow_down = [
    e, e, e, b, b, e, e, e,
    e, e, e, b, b, e, e, e,
    e, e, e, b, b, e, e, e,
    e, e, e, b, b, e, e, e,
    b, e, e, b, b, e, e, b,
    e, b, e, b, b, e, b, e,
    e, e, b, b, b, b, e, e,
    e, e, e, b, b, e, e, e
]
bars = [
    e, e, e, e, e, e, e, e,
    e, e, e, e, e, e, e, e,
    r, r, r, r, r, r, r, r,
    r, r, r, r, r, r, r, r,
    b, b, b, b, b, b, b, b,
    b, b, b, b, b, b, b, b,
    e, e, e, e, e, e, e, e,
    e, e, e, e, e, e, e, e
]

class Station():

  def __init__(self, name, station_id, station_key):
    self.name = name
    self.id = station_id
    self.key = station_key
    self.sense = SenseHat()


  def c_to_f(self,input_temp):
    # convert input_temp from Celsius to Fahrenheit
    return (input_temp * 1.8) + 32


  def get_cpu_temp(self):
    # 'borrowed' from https://www.raspberrypi.org/forums/viewtopic.php?f=104&t=111457
    # executes a command at the OS to pull in the CPU temperature
    res = os.popen('vcgencmd measure_temp').readline()
    return float(res.replace("temp=", "").replace("'C\n", ""))


  # use moving average to smooth readings
  def get_smooth(self,x):
    # do we have the t object?
    if not hasattr(self.get_smooth, "t"):
        # then create it
        self.get_smooth.t = [x, x, x]
    # manage the rolling previous values
    self.get_smooth.t[2] = self.get_smooth.t[1]
    self.get_smooth.t[1] = self.get_smooth.t[0]
    self.get_smooth.t[0] = x
    # average the three last temperatures
    xs = (self.get_smooth.t[0] + self.get_smooth.t[1] + self.get_smooth.t[2]) / 3
    return xs


  def get_temp(self):
    # ====================================================================
    # Unfortunately, getting an accurate temperature reading from the
    # Sense HAT is improbable, see here:
    # https://www.raspberrypi.org/forums/viewtopic.php?f=104&t=111457
    # so we'll have to do some approximation of the actual temp
    # taking CPU temp into account. The Pi foundation recommended
    # using the following:
    # http://yaab-arduino.blogspot.co.uk/2016/08/accurate-temperature-reading-sensehat.html
    # ====================================================================
    # First, get temp readings from both sensors
    t1 = self.sense.get_temperature_from_humidity()
    t2 = self.sense.get_temperature_from_pressure()
    # t becomes the average of the temperatures from both sensors
    t = (t1 + t2) / 2
    # Now, grab the CPU temperature
    t_cpu = self.get_cpu_temp()
    # Calculate the 'real' temperature compensating for CPU heating
    t_corr = t - ((t_cpu - t) / 1.5)
    # Finally, average out that value across the last three readings
    t_corr = self.get_smooth(t_corr)
    return t_corr

  def broadcast_info(self,info):
    try:
        #upload_url = SERVER_URL + "?" + urlencode(info)
        response = requests.post(SERVER_URL, data=info)
        print(response.status_code, response.reason)
        response.close()  # best practice to close the file
    except:
        print("Exception:", sys.exc_info()[0])

  def start_station(self):
    weather_data = {}
    # initialize the lastMinute variable to the current time to start
    last_minute = datetime.datetime.now().minute
    # on startup, just use the previous minute as lastMinute
    last_minute -= 1
    if last_minute == 0:
        last_minute = 59

    # infinite loop to continuously check weather values
    while 1:
        current_second = datetime.datetime.now().second

        if (current_second == 0) or ((current_second % 5) == 0):
            # ========================================================
            # read values from the Sense HAT
            # ========================================================
            # Calculate the temperature. The get_temp function 'adjusts' the recorded temperature adjusted for the
            # current processor temp in order to accommodate any temperature leakage from the processor to
            # the Sense HAT's sensor. This happens when the Sense HAT is mounted on the Pi in a case.
            # If you've mounted the Sense HAT outside of the Raspberry Pi case, then you don't need that
            # calculation. So, when the Sense HAT is external, replace the following line (comment it out  with a #)
            calc_temp = self.sense.get_temperature()
            # with the following line (uncomment it, remove the # at the line start)
            # calc_temp = sense.get_temperature_from_pressure()
            # or the following line (each will work)
            # calc_temp = sense.get_temperature_from_humidity()
            # ========================================================
            # At this point, we should have an accurate temperature, so lets use the recorded (or calculated)
            # temp for our purposes
            temp_c = round(calc_temp, 1)
            temp_f = round(self.c_to_f(calc_temp), 1)
            humidity = round(self.sense.get_humidity(), 0)
            # convert pressure from millibars to inHg before posting
            pressure = round(self.sense.get_pressure() * 0.0295300, 1)
            print("Temp: %sF (%sC), Pressure: %s inHg, Humidity: %s%%" % (temp_f, temp_c, pressure, humidity))
            weather_data = {
                "action": "updateraw",
                "ID": self.id,
                "PASSWORD": self.key,
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
            self.broadcast_info(user_data)
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
                            self.sense.set_pixels(arrow_down)
                        else:
                            # display a red, up arrow
                            self.sense.set_pixels(arrow_up)
                    else:
                        # temperature stayed the same
                        # display red and blue bars
                        self.sense.set_pixels(bars)
                    # set last_temp to the current temperature before we measure again
                    last_temp = temp_f

                    # is weather upload enabled (True)?
                    if WEATHER_UPLOAD:
                        # From http://wiki.wunderground.com/index.php/PWS_-_Upload_Protocol
                        print("Uploading data to Weather Underground")
                        # build a weather data object
                        weather_data = {
                            "action": "updateraw",
                            "ID": self.id,
                            "PASSWORD": self.key,
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