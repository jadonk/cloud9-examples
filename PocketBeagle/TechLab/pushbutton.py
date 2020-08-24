#!/usr/bin/python3
#//////////////////////////////////////
#	pushbutton.py
#	Reads the Left push button.
#//////////////////////////////////////
import Adafruit_BBIO.GPIO as GPIO
import time

button = "P2_33"        # L button

GPIO.setup(button, GPIO.IN)
 
def doRead(channel):
    print('Edge detected  %s'%channel)
 
GPIO.add_event_detect(button, GPIO.BOTH, callback=doRead)

print("Ready. Please press 'L' button on TechLab. Hit ^C to stop.");

time.sleep(30)     # Do something while waiting for event
    
GPIO.cleanup()
