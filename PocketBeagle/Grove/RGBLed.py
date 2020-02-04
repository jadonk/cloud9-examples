#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# [Grove - Chainable RGB LED X 2](http://wiki.seeedstudio.com/Grove-Chainable_RGB_LED/) on A2
import time
from Shell import GetCmdReturn,os

class P981X:
    def __init__(self, leds = 2):
        try:
            if not os.path.exists('/proc/device-tree/p981x_1057@20'):
                GetCmdReturn('sudo mkdir -p \
                /sys/kernel/config/device-tree/overlays/BB-GPIO-P9813')
                GetCmdReturn('sudo dd \
                of=/sys/kernel/config/device-tree/overlays/BB-GPIO-P9813/dtbo \
                if=/lib/firmware/BB-GPIO-P9813.dtbo')
                while not os.path.exists('/proc/device-tree/p981x_1057@20'):
                    time.sleep(0.1)
            if not os.path.exists('/dev/p981x0'):
                mod_path = '/lib/modules/'+GetCmdReturn('uname -r')+'/extra/seeed/p9813.ko'
                subprocess.call(['sudo', 'insmod', mod_path])             
                while not os.path.exists('/dev/p981x0'):
                    time.sleep(0.1)
            self.f = open('/dev/p981x0', 'w')
            # defult leds = 2 
            self.f.write('N %d\n'%leds)
            self.f.flush()
        except IOError as err:
            print("File Error:"+str(err))
            print("maybe you should reinstall the driver of p981x")

    def set(self, led, red, green, blue):
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
