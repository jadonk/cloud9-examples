#!/usr/bin/python3
#//////////////////////////////////////
#	analogInOut.py
# 	Reads analog in on P9_36 and adjusts the PWM on P9_14.
# 	Wiring:	Attach the outer pins on a variable resistor to P9_32 and P9_34.
#          Attach the wiper (middle pin) of the resistor to P9_37.
#          P9_14 connects to the plus lead of an LED.  The negative lead of the
# 			LED goes to a 220 Ohm resistor.  The other lead of the resistor goes
# 			to ground.
#//////////////////////////////////////
import Adafruit_BBIO.PWM as PWM
import Adafruit_BBIO.ADC as ADC
import time
ADC.setup()

inputPin  = "P9_37"
outputPin = "P9_14"

print('Hit ^C to stop')

PWM.start(outputPin, 1)

while True:
    x = ADC.read(inputPin)
    PWM.set_duty_cycle(outputPin, 100*x)
    print('{}: {:.1f}%, {:.3f} V'.format(inputPin, 100*x, 1.8*x), end = '\r')
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