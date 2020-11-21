#!/usr/bin/env python
# ////////////////////////////////////////
# //	seqLED.py
# //      Blinks the USR LEDs in sequence.
# //	Wiring:
# //	Setup:	
# //	See:	
# ////////////////////////////////////////
import Adafruit_BBIO.GPIO as GPIO
import time

LEDs=4

for i in range(LEDs):
    GPIO.setup("USR%d" % i, GPIO.OUT)

while True:
    for i in range(LEDs):
        GPIO.output("USR%d" % i, GPIO.HIGH)
        time.sleep(0.25)
    for i in range(LEDs):
        GPIO.output("USR%d" % i, GPIO.LOW)
        time.sleep(0.25)