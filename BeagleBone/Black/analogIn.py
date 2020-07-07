#!/usr/bin/python3
#//////////////////////////////////////
#	analogin.py
# 	Reads the analog value of the light sensor.
#//////////////////////////////////////
import Adafruit_BBIO.ADC as ADC
import time
ADC.setup()

pin = "P9_37"        # light sensor

print('Hit ^C to stop')

while True:
    x = ADC.read(pin)
    print('{}: {:.1f}%, {:.3f} V'.format(pin, 100*x, 1.8*x), end = '\r')
    time.sleep(0.1)
