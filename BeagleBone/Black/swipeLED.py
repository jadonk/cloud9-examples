#!/usr/bin/python3
#//////////////////////////////////////
#	swipeLED.py
#      Blinks the USR LEDs in sequence.
#//////////////////////////////////////
import Adafruit_BBIO.GPIO as GPIO
import time

leds = ['USR0', 'USR1', 'USR2', 'USR3']
i = 0;
delay = 0.1;

print('Hit ^C to stop')

print("Toggling LEDs:")
for x in leds:
    GPIO.setup(x, GPIO.OUT)
    print("0", end='');
    
def n(i):
    if i >= len(leds) :
        return 2*len(leds)-i-2
    else:
        return i

while True:
    # Turn LED on
    print("\x1b[" + str(n(i)+1) + "G1", end='', flush=True);
    GPIO.output(leds[n(i)], GPIO.HIGH)
    time.sleep(delay)

    # Turn LED off
    print("\x1b[" + str(n(i)+1) + "G0", end='', flush=True)
    GPIO.output(leds[n(i)], GPIO.LOW)
    i = i +1
    if i >= 2*len(leds)-2:
        i = 0
