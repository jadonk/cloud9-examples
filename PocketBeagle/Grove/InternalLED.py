#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# Nothing to plug in.
import time
state = 0 # Initial state
led = open('/sys/class/leds/beaglebone:green:usr3/brightness', 'w')
while True:
  print(state, file=led)
  led.flush()
  if(state == 1):
    state = 0
  else:
    state = 1
  time.sleep(0.25)
