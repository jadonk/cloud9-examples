#!/usr/bin/env python3
# ////////////////////////////////////////
# //	input.py
# //      Responds to changes on P8_19 via a callback.
# //	Wiring:	Connect a switch between inputPin and 3.3V
# //            Attach and LED through a 220 Ohm resistor to outputPin
# //	Setup:	
# //	See:	
# ////////////////////////////////////////
import Adafruit_BBIO.GPIO as GPIO
import time

outputPin = "P9_14";
inputPin  = "P8_14";
ledPin    = "USR3";
state   = 0;

# Set the direction on the pins
GPIO.setup(outputPin, GPIO.OUT)
GPIO.setup(ledPin,    GPIO.OUT)
GPIO.setup(inputPin,  GPIO.IN)

# This calback is called everytime the input changes
# channel is the name of the pin that changed
def my_callback(channel):
    # Read the current value of the input
    state = GPIO.input(channel)
    print('Edge detected on channel {}, value={}'.format(channel, state))
    # Write it out
    GPIO.output(outputPin, state)
    GPIO.output(ledPin, state)

# This is a non-blocking event 
GPIO.add_event_detect(inputPin, GPIO.BOTH, callback=my_callback) 

try:
    while True:             # Do something while waiting for event
        time.sleep(100)

except KeyboardInterrupt:
    print("Cleaning up...")
    GPIO.cleanup()
