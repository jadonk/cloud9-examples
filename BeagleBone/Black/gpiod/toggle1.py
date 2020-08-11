#!/usr/bin/env python3
# //////////////////////////////////////
# 	toggle.c
#  Toggles the P9_14 pin as fast as it can. P9_14 is line 18 on chip 1.
# 	Wiring:	Attach an oscilloscope to P9_14 to see the squarewave or 
#          uncomment the usleep and attach an LED.
# 	Setup:	sudo apt uupdate; pip3 install gpiod
# 	See:	https://pypi.org/project/gpiod/0.5.4/
# //////////////////////////////////////

import gpiod
import sys
import time

if len(sys.argv) > 2:
    LED_CHIP = sys.argv[1]
    LED_LINE_OFFSET = int(sys.argv[2])
else:
    print('''Usage:\npython3 blink.py <chip> <line offset>''')
    LED_CHIP = 1
    LED_LINE_OFFSET = 18  # P9_14
    # sys.exit()

chip = gpiod.chip(LED_CHIP)
led = chip.get_line(LED_LINE_OFFSET)

config = gpiod.line_request()
config.consumer = "Blink"
config.request_type = gpiod.line_request.DIRECTION_OUTPUT

led.request(config)

while True:
    led.set_value(0)
    # time.sleep(0.1)
    led.set_value(1)
    # time.sleep(0.1)