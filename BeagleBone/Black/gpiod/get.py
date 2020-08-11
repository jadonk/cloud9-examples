#!/usr/bin/env python3
# Based on https://git.kernel.org/pub/scm/libs/libgpiod/libgpiod.git/tree/bindings/python/examples

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
