#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# Exploring iio library

import iio
import time

contexts = iio.scan_contexts()
print("contexts: ",end='')
print(contexts)

ctx = iio.Context("local:") 
print("ctx: ", end='')
print(ctx)
# help(ctx)
print(ctx.devices)

for dev in ctx.devices:
    print(dev)
    print(dev.name)
    print(dev.id)
    # help(dev)

dev = ctx.find_device("adxl345")

print(dev.channels)
for chan in dev.channels:
    # help(chan)
    # print(chan.name)
    print(chan.id)

chan = dev.find_channel("accel_x", False)
print(chan.id)
print(chan.attrs)
x = chan.attrs["raw"]

while True:
    print(x.value)
    time.sleep(0.25)