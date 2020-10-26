#!/usr/bin/env python3
# Read a TMP101 sensor

import smbus
import time

bus = smbus.SMBus(2)    # Bus Number
address = 0x48          # Device address

while True:
    temp = bus.read_byte_data(address, 0) # 0 is register to read
    print(temp, end="\r")
    time.sleep(0.25)
