#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# [Grove - Chainable RGB LED X 2](http://wiki.seeedstudio.com/Grove-Chainable_RGB_LED/) on A2
import time
from Shell import InstallDTBO
import os
class P981X:
    """P981X RGB LED Driver"""
    def __init__(self, leds = 2):
        """Initialize the P981X using file python library
            leds:the LED's chain length (defult leds = 2)
        """
        try:
            # Check BB-GPIO-P9813 whether install successfully
            # if not reinstall it             
            if not os.path.exists('/proc/device-tree/p981x_1057@20'):
                InstallDTBO('BB-GPIO-P9813')
                while not os.path.exists('/proc/device-tree/p981x_1057@20'):
                    time.sleep(0.1)
            #Open the /dev/p981x0 using file python library             
            self.f = open('/dev/p981x0', 'w')
            #Set the LED's chain length
            self.f.write('N %d\n'%leds)
            self.f.flush()
        except IOError as err:
            print("File Error:"+str(err))
            print("maybe you should reinstall the driver of p981x")
    def set(self, led, red, green, blue):
        """Set LED's value of R,G,B
            led:which one on LED's chain(defult 0 or 1)
            red:The value that describes R of R,G,B(0~255)
            green:The value that describes G of R,G,B(0~255)
            blue:The value that describes B of R,G,B(0~255)
        """
        try:
            self.f.write('D %d %d %d %d\n'%(led,red,green,blue))
            self.f.flush()
        except IOError as err:
            print("File Error:"+str(err))
            print("maybe you should reinstall the driver of p981x")
def main():
    LED = P981X()
    while True:
        LED.set(0,0x20,0,0)
        LED.set(1,0,0x20,0)
        time.sleep(0.25)
        LED.set(0,0,0x20,0)
        LED.set(1,0x20,0,0)
        time.sleep(0.25)
if __name__ == "__main__":
    main()