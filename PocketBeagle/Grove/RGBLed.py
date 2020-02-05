# Copyright (c) 2020 SeeedStudio
# Author: Hansen Chen
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# [Grove - Chainable RGB LED X 2](http://wiki.seeedstudio.com/Grove-Chainable_RGB_LED/) on A2
import time
from Shell import GetCmdReturn,os

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
                GetCmdReturn('sudo mkdir -p \
                /sys/kernel/config/device-tree/overlays/BB-GPIO-P9813')
                GetCmdReturn('sudo dd \
                of=/sys/kernel/config/device-tree/overlays/BB-GPIO-P9813/dtbo \
                if=/lib/firmware/BB-GPIO-P9813.dtbo')
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
