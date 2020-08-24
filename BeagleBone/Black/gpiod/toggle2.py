#!/usr/bin/env python3
# //////////////////////////////////////
# 	toggle2.py
#  Toggles P9_14 and P9_16 pins as fast as it can. 
# 	P9_14 and P9_16 are both on chip 1 so they can be toggled together.
# 	P9_14 is line 18 P9_16 is line 18.
# 	Wiring:	Attach an oscilloscope to P9_14 and P9_16  to see the squarewave or 
#          uncomment the usleep and attach an LED.
# 	Setup:	sudo apt uupdate; pip3 install gpiod
# 	See:	https://git.kernel.org/pub/scm/libs/libgpiod/libgpiod.git/tree/bindings/python/examples
# //////////////////////////////////////

import gpiod
import time

LED_CHIP = 'gpiochip1'
LED_LINE_OFFSET = [18, 19]  # P9_14 and P9_16

chip = gpiod.Chip(LED_CHIP)

lines = chip.get_lines(LED_LINE_OFFSET)
lines.request(consumer='blink', type=gpiod.LINE_REQ_DIR_OUT)

while True:
    lines.set_values([0, 0])
    # time.sleep(0.1)
    lines.set_values([1, 1])
    # time.sleep(0.1)
