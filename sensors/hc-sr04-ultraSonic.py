#!/usr/bin/env python3

# This is an example of reading HC-SR04 Ultrasonic Range Finder
# This version measures from the fall of the Trigger pulse 
#   to the end of the Echo pulse
# Check the timing to be sure it calibrated.

import Adafruit_BBIO.GPIO as GPIO
import time

trigger = 'P9_15'    # Pin to trigger the ultrasonic pulse
echo    = 'P9_17'    # Pin to measure to pulse width related to the distance
ms = 1000            # Trigger period in ms

GPIO.setup(trigger, GPIO.OUT)
GPIO.setup(echo, GPIO.IN)

# Called when falling edte of pulse is detected
def pingEnd(channel):
    global startTime
    # print('Edge detected on channel %s'%channel)
    totalTime = time.perf_counter() - startTime
    print('totalTime = {0:0.2f}'.format(1000*totalTime))
    # startTime = time.perf_counter()

GPIO.add_event_detect(echo, GPIO.FALLING, callback=pingEnd) 

# Pulse trigger high then low and start timing.
while True:             # Do something while waiting for event
    # print('ping')
    GPIO.output(trigger, 1)
    time.sleep(0.005)
    GPIO.output(trigger, 0)
    startTime = time.perf_counter()
    time.sleep(ms/1000)         # Wait and let callback to the work
    
GPIO.cleanup()
