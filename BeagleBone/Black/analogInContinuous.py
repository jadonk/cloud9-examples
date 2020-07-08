#!/usr/bin/python3
#//////////////////////////////////////
#	analogInContinuous.py
# 	Read analog data vioa IIO continous mode and plots it.
#//////////////////////////////////////

# From: https://stackoverflow.com/questions/20295646/python-ascii-plots-in-terminal
# https://github.com/dkogan/gnuplotlib
# https://github.com/dkogan/gnuplotlib/blob/master/guide/guide.org
# sudo apt install gnuplot
# pip3 install gnuplotlib

import numpy      as np
import gnuplotlib as gp
import time
import struct

IIOPATH='/sys/bus/iio/devices/iio:device0'
IIODEV='/dev/iio:device0'
LEN = 100
SAMPLERATE=8000

# Setup IIO for Continous reading
# Enable AIN1, which isn P9_40
try:
    file1 = open(IIOPATH+'/scan_elements/in_voltage1_en', 'w')     # P9_40
    file1.write('1') 
    file1.close()
except:     # carry on if it's already enabled
    pass
# Set buffer length
file1 = open(IIOPATH+'/buffer/length', 'w')
file1.write(str(2*LEN))     # I think LEN is in 16-bit values, but here we pass bytes
file1.close()
# Enable continous
file1 = open(IIOPATH+'/buffer/enable', 'w')
file1.write('1')
file1.close()

fd = open(IIODEV, "r")

print('Hit ^C to stop')

x = np.linspace(0, 1000*LEN/SAMPLERATE, LEN)

try:
    while True:
        y = np.fromfile(fd, dtype='uint16', count=LEN)
        # print(y)
        gp.plot(x, y,
            xlabel = 't (ms)',
            _yrange = [0, 4100],
            title  = 'analogInContinuous',
            legend = np.array( ("P9.40", "P9.38"), ),
            # _with  = 'lines'
            )

except KeyboardInterrupt:
    print("Turning off input.")
    # Disable continous
    file1 = open(IIOPATH+'/buffer/enable', 'w')
    file1.write('0')
    file1.close()
