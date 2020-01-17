#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# [Grove - 16x2 LCD](http://wiki.seeedstudio.com/Grove-16x2_LCD_Series/) on I2C1
import time
import subprocess
import os

class LCD:
    def __init__(self, leds):
        try:
            if not os.path.exists('/proc/device-tree/aliases/jhd1802'):
                subprocess.call(['sudo', 'mkdir', '-p',
                    '/sys/kernel/config/device-tree/overlays/BB-I2C1-JHD1802'])
                subprocess.call(['sudo', 'dd',
                    'of=/sys/kernel/config/device-tree/overlays/BB-I2C1-JHD1802/dtbo',
                    'if=/lib/firmware/BB-I2C1-JHD1802.dtbo'])
                time.sleep(0.1)
            if not os.path.exists('/dev/lcd0'):
                subprocess.call(['sudo', 'modprobe', 'hd44780'])
                time.sleep(0.1)
            try:
                self.f = open('/dev/lcd0', 'w')
            except IOError as err:
                subprocess.call(['sudo', 'chmod', '777', '/dev/lcd0'])
                self.f = open('/dev/lcd0', 'w')
        except IOError as err:
            print("File Error:"+str(err))
            print("maybe you should reinstall the driver of hd44780")
    def set(self, text):
        try:
            self.f.write('\x1b[2J')
            self.f.write('\x1b[H')
            self.f.write('%s'%text)
            self.f.flush()
        except IOError as err:
            print("File Error:"+str(err))
            print("maybe you should reinstall the driver of hd44780")

def main():
    d = LCD(2)
    while True:
        d.set("abcdefghijklmnopqrstuvwxyz012345")
        time.sleep(0.25)
        d.set("ABCDEFGHIJKLMNOPQRSTUVWXYZ6789!@")
        time.sleep(0.25)

if __name__ == "__main__":
    main()