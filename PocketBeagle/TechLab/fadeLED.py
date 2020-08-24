#!/usr/bin/python3
#//////////////////////////////////////
# 	fadeLED.py
# 	Fades the blue LED on and off.
#//////////////////////////////////////
import Adafruit_BBIO.PWM as PWM
import time
LED = 'P1_36'   # Red = P1_33, Green = P2_1, Blue = P1_36
step = 10       # Step size
min =  0        # dimmest value
max =  100      # brightest value
brightness = min # Current brightness;
 
PWM.start(LED, brightness)

while True:
    PWM.set_duty_cycle(LED, brightness)
    brightness += step
    if(brightness >= max or brightness <= min):
        step = -1 * step
    time.sleep(0.04)
