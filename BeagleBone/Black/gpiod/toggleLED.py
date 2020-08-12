#!/usr/bin/env python3
# //////////////////////////////////////
# 	toggleLED.py
#   Toggles the four built in USR LEDs 
# 	They are all on chip 1 so they can be toggled together.
# 	Setup:	sudo apt uupdate; pip3 install gpiod
# 	See:	https://git.kernel.org/pub/scm/libs/libgpiod/libgpiod.git/tree/bindings/python/examples
# //////////////////////////////////////
import gpiod
import time

LED_CHIP = 'gpiochip1'
LED_LINE_OFFSET = [21, 22, 23, 24]  # USR LEDS 1-4

chip = gpiod.Chip(LED_CHIP)

lines = chip.get_lines(LED_LINE_OFFSET)
lines.request(consumer='blink', type=gpiod.LINE_REQ_DIR_OUT)

while True:
    lines.set_values([0, 0, 0, 0])
    time.sleep(0.25)
    lines.set_values([1, 1, 1, 1])
    time.sleep(0.25)
