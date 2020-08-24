#!/usr/bin/env python3
# //////////////////////////////////////
# 	get.py
#  Get the value of P8_13. P8_13 is line 23 on chip 0.
# 	Wiring:	Attach a switch to P8_13 and 3.3V
# 	Setup:	sudo apt uupdate; sudo apt install libgpiod-dev
# 	See:	https://github.com/starnight/libgpiod-example/blob/master/libgpiod-led/main.c
# //////////////////////////////////////

import gpiod
import sys

if len(sys.argv) < 3:   # Use P8_13 if not given
    CHIP='0'
    offsets=[23]
else:
    CHIP=sys.argv[1]
    offsets = []
    for off in sys.argv[2:]:
        offsets.append(int(off))
    
chip = gpiod.Chip(CHIP)

lines = chip.get_lines(offsets)
lines.request(consumer=sys.argv[0], type=gpiod.LINE_REQ_DIR_IN)

print("Hit ^C to stop")

while True:
    vals = lines.get_values()
    
    for val in vals:
        print(val, end=' ')
    print('\r', end='')
