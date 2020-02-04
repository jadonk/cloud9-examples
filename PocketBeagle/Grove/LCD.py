#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# [Grove - 16x2 LCD](http://wiki.seeedstudio.com/Grove-16x2_LCD_Series/) on I2C1
import time
from Shell import GetCmdReturn,os
class JHD1802:
    def __init__(self):
        try:
            if not os.path.exists('/proc/device-tree/aliases/jhd1802'):
                GetCmdReturn('sudo mkdir -p \
                /sys/kernel/config/device-tree/overlays/BB-I2C1-JHD1802')
                GetCmdReturn('sudo dd \
                of=/sys/kernel/config/device-tree/overlays/BB-I2C1-JHD1802/dtbo \
                if=/lib/firmware/BB-I2C1-JHD1802.dtbo')
                while not os.path.exists('/proc/device-tree/aliases/jhd1802'):
                    time.sleep(0.1)
                    
            if 'hd44780' in GetCmdReturn('lsmod | grep hd44780'):
                GetCmdReturn('sudo rmmod hd44780')  
            while 'hd44780' in GetCmdReturn('lsmod | grep hd44780'):
                time.sleep(0.1)   
            
            GetCmdReturn('sudo modprobe -i hd44780')
            while not 'hd44780' in GetCmdReturn('lsmod | grep hd44780'):
                time.sleep(0.1) 
                
            try:
                self.f = open('/dev/lcd0', 'w')
            except IOError as err:
                GetCmdReturn('sudo chmod 777 /dev/lcd0')
                self.f = open('/dev/lcd0', 'w')
            self.f.write('\x1b[2J')
            self.f.write('\x1b[H')
            self.f.flush()
        except IOError as err:
            print("File Error:"+str(err))
            print("maybe you should reinstall the driver of hd44780")
    def SetText(self, text):
        try:
            with open('/dev/lcd0', 'w') as f:
                # f.write('\x1b[2J')
                f.write('\x1b[H')
                f.write('%s'%text)
        except IOError as err:
            print("File Error:"+str(err))
            print("maybe you should reinstall the driver of hd44780")

def main():
    d = JHD1802()
    d.SetText("abcdefghijklmnopqrstuvwxyz012345")
    time.sleep(0.25)
    d.SetText("ABCDEFGHIJKLMNOPQRSTUVWXYZ6789!@")
    time.sleep(0.25)

if __name__ == "__main__":
    main()
