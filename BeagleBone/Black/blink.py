#!/usr/bin/python
#//////////////////////////////////////
#	blink.py
#	Blinks one LED wired to P9_14.
#	Wiring:	P9_14 connects to the plus lead of an LED.  The negative lead of the
#			LED goes to a 220 Ohm resistor.  The other lead of the resistor goes
#			to ground.
#	Setup:	
#	See:	
#//////////////////////////////////////
import Adafruit_BBIO.GPIO as GPIO
import time

out = "P9_14"
 
GPIO.setup(out, GPIO.OUT)
 
while True:
    GPIO.output(out, GPIO.HIGH)
    time.sleep(0.5)
    GPIO.output(out, GPIO.LOW)
    time.sleep(0.5)
