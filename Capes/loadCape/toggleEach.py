#!/usr/bin/env python3
# 
# Copyright (C) 2020 Deepak Khatri <deepaklorkhatri7@gmail.com>
# https://lorforlinux.github.io/GSoC2020_BeagleBoard.org/
#
# This program will toggle each load (Blink each RED led on the cape)
# To use this, Load Cape overlay must be loaded automatically/manually 
# 
# If automatically loaded you must see "BBORG_LOAD-00A2" under
# directory -> /proc/device-tree/chosen/overlays/
# 
# To load the overlay manually you must edit "/boot/uEnv.txt" with
# ...
# enable_uboot_overlays=1
# uboot_overlay_addr0=BBORG_LOAD-00A2.dtbo
# ...
#

import time

def loadON(i):
	'''
	This function will turn ON the load
	loadON(i) where i = loadSink index (1-9)
	'''
    sink = open("/sys/class/leds/load-sink"+str(i)+"/brightness", "w")    
    sink.write("255")
    sink.close()

def loadOFF(i):
	'''
	This function will turn OFF the load
	loadOFF(i) where i = loadSink index (1-9)
	'''
    sink = open("/sys/class/leds/load-sink"+str(i)+"/brightness", "w")    
    sink.write("0")
    sink.close()

# toggling each load
for i in range(1, 9):
	# print message
    print("Toggling Sink{}".format(i))
	# turn on load i
    loadON(i)
	# wait for 1/2 second
    time.sleep(0.5)
	# turn off load i
    loadOFF(i)
	# wait for 1/2 second
    time.sleep(0.5)