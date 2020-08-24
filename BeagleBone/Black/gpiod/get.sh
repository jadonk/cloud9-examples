#!/bin/bash
# Reads P8_13 via gpiod.  P8_13 is chip 0 line 23

echo Hit ^c to stop

while true; do 
	gpioget 0 23 | tr \\n \\r
done