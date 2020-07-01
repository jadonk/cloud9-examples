#!/usr/bin/python3
#//////////////////////////////////////
#	accelerometer.py
#	Reads the MMA8453Q, 3-axis, 10-bit/8-bit digital accelerometer
#   See: https://www.nxp.com/docs/en/data-sheet/MMA8453Q.pdf
#//////////////////////////////////////
import time

path = '/sys/class/i2c-adapter/i2c-2/2-001c/iio:device1'

fdx = open(path + '/in_accel_x_raw', 'r')
fdy = open(path + '/in_accel_y_raw', 'r')
fdz = open(path + '/in_accel_z_raw', 'r')

print('  x     y     z')
 
while True:
    fdx.seek(0, 0)      # Back to the start
    fdy.seek(0, 0)
    fdz.seek(0, 0)
    x = fdx.read()[:-1]  # Remove \n
    y = fdy.read()[:-1]
    z = fdz.read()[:-1]

    print('{:>4}, {:>4}, {:>4}'.format(x, y, z), end='\r')
    time.sleep(0.1)