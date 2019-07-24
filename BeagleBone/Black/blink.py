#!/usr/bin/python
import Adafruit_BBIO.GPIO as GPIO
import time

out = "P9_25"
 
GPIO.setup(out, GPIO.OUT)
 
while True:
    GPIO.output(out, GPIO.HIGH)
    time.sleep(0.5)
    GPIO.output(out, GPIO.LOW)
    time.sleep(0.5)
