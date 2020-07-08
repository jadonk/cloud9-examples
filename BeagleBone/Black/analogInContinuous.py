#!/usr/bin/python3
#//////////////////////////////////////
#	analogin.py
# 	Reads the analog value of the light sensor.
#//////////////////////////////////////
# import Adafruit_BBIO.ADC as ADC
# import time
# ADC.setup()

# pin = "P9_37"        # light sensor

# print('Hit ^C to stop')

# while True:
#     x = ADC.read(pin)
#     print('{}: {:.1f}%, {:.3f} V'.format(pin, 100*x, 1.8*x), end = '\r')
#     time.sleep(0.1)

# From: https://stackoverflow.com/questions/20295646/python-ascii-plots-in-terminal
# sudo apt install gnuplot
# pip3 install gnuplotlib

import numpy      as np
import gnuplotlib as gp
import time
import struct

IIOPATH='/sys/bus/iio/devices/iio:device0'
IIODEV='/dev/iio:device0'

fd = open(IIODEV, "r")

while True:
    x = np.fromfile(fd, dtype='uint16', count=256)
    # print(x)
    # x = np.arange(101) - 50
    gp.plot(x)

# Frpm: https://hplgit.github.io/scitools/doc/api/html/aplotter.html
# pip3 install scitools
# from scitools.aplotter import plot
# from numpy import linspace, exp, cos, pi
# x = linspace(-2, 2, 81)
# y = exp(-0.5*x**2)*cos(pi*x)
# plot(x, y)