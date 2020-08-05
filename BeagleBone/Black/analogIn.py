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

# // Bone  | Pocket | AIN
# // ----- | ------ | --- 
# // P9_39 | P1_19  | 0
# // P9_40 | P1_21  | 1
# // P9_37 | P1_23  | 2
# // P9_38 | P1_25  | 3
# // P9_33 | P1_27  | 4
# // P9_36 | P2_35  | 5
# // P9_35 | P1_02  | 6