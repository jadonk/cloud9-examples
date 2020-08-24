#!/usr/bin/python3
#//////////////////////////////////////
#	internalLED.py
#	Blinks the USR3 internal LED.
#//////////////////////////////////////
import Adafruit_BBIO.GPIO as GPIO
import time

out = "USR3"
 
GPIO.setup(out, GPIO.OUT)
 
while True:
    GPIO.output(out, GPIO.HIGH)
    time.sleep(0.25)
    GPIO.output(out, GPIO.LOW)
    time.sleep(0.25)
