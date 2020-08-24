# Author: Deepak Khatri <deepaklorkhatri7@gmail.com>
# Part of GSoC 2020 Project 'Cape compatibility layer for BeagleBone Black and BeagleBone AI'
# Reference: https://stackoverflow.com/questions/676172/full-examples-of-using-pyserial-package
#
# See cape interface spec page for UART for more info on Bone UART
# https://elinux.org/Beagleboard:BeagleBone_cape_interface_spec#UART
#
# Requires pyserial, Install using: pip3 install pysreial

import serial
import time

# setup Bone UART
ser = serial.Serial( port = "/dev/bone/uart/1", baudrate=110052)
# Refresh connection
ser.close()
ser.open()

# Welcome message
print("Welcome to UART console\r\nInsert \"exit\" to leave the application.\r\n")
# ser.write(str.encode("Hello World!"))

while 1 :
    # get keyboard input for TX
    TX = input(">> ")
    if TX == 'exit':
        ser.close()
        exit()
    else:
        # send the character to the device
        ser.write(str.encode(TX + '\r\n'))
        RX = ''
        # wait before reading
        time.sleep(0.1)
        while ser.inWaiting() > 0:
            RX += str(ser.read(1).decode('utf-8'))
        # print RX
        if RX != '':
            print("<< " + RX)