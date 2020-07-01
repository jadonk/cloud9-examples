#!/usr/bin/python3
#//////////////////////////////////////
#	buzzer.py
#	Buzzes the buzzer
#   The buzzer is just a speaker so you have to keep toggling the GPIO pin
#   Setup:  config-pin P2_30 out
#//////////////////////////////////////
import Adafruit_BBIO.GPIO as GPIO
import time

buzzer = 'P2_30'
GPIO.setup(buzzer, GPIO.OUT)

for i in range(500):
    GPIO.output(buzzer, GPIO.HIGH)
    time.sleep(0.001)
    GPIO.output(buzzer, GPIO.LOW)
    time.sleep(0.001)
    
GPIO.cleanup()