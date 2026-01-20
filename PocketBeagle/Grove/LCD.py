#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# [Grove - 16x2 LCD](http://wiki.seeedstudio.com/Grove-16x2_LCD_Series/) on I2C1
import time
from Shell import ReinstallModule,InstallDTBO,GetCmdReturn
import os
class JHD1802:
    """JHD1802 LCD Driver"""
    def __init__(self):
        """Initialize the JHD1802 using file python library"""
        self.Path = '/proc/device-tree/aliases/jhd1802'
        self.Lcd0 = '/dev/lcd0'
        try:
            # Check BB-I2C1-JHD1802 whether install successfully
            # if not reinstall it             
            if not os.path.exists(self.Path):
                InstallDTBO('BB-I2C1-JHD1802')
                while not os.path.exists(self.Path):
                    time.sleep(0.1)
            #Reinstall hd44780 module to support hot plug        
            ReinstallModule('seeed-hd44780')
            try:
                #Open the /dev/lcd0 using file python library
                self.f = open(self.Lcd0, 'w')
            except IOError as err:
                GetCmdReturn('sudo chmod 777 %s'%self.Lcd0)
                self.f = open(self.Lcd0, 'w')
            #Clean LCD 
            self.f.write('\x1b[2J')
            self.f.write('\x1b[H')
            self.f.flush()
        except IOError as err:
            print("File Error:"+str(err))
            print("maybe you should reinstall the driver of hd44780")
    def SetText(self, text):
        """Display the string on LCD
           text:content on LCD
        """
        try:
            self.f.write('\x1b[H')
            self.f.flush()
            self.f.write('%s'%text)
            self.f.flush()
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