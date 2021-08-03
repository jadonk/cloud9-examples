#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# [Grove - 16x2 LCD](http://wiki.seeedstudio.com/Grove-16x2_LCD_Series/) on I2C1
# Displays the fir 6 ADC values on the LCD.
import iio
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
            time.sleep(1)       # Let the startup message show
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

class ADC:
    """ADC of PocketBeagle"""
    def __init__(self):
        """Initialize the ADC of PocketBeagle using iio python library
        """    
        self.AIN = []
        #Scan the ADC of PocketBeagle by using IIO python library
        # self.contexts = iio.scan_contexts()
        self.ctx = iio.Context("local:")
        for dev in self.ctx.devices:
            if 'adc.0.auto' in dev.name:
                self.name = dev.name
        self.dev = self.ctx.find_device(self.name)
        if not self.dev:
            print("maybe you should reinstall the driver of ADC")
            return
        #Integrate all channels to self.AIN
        self.AIN.append(self.dev.find_channel("voltage0", False))
        self.AIN.append(self.dev.find_channel("voltage1", False))
        self.AIN.append(self.dev.find_channel("voltage2", False))
        self.AIN.append(self.dev.find_channel("voltage3", False))
        self.AIN.append(self.dev.find_channel("voltage4", False))
        self.AIN.append(self.dev.find_channel("voltage5", False))
        self.AIN.append(self.dev.find_channel("voltage6", False))
        self.AIN.append(self.dev.find_channel("voltage7", False))
    def get(self, n):
        """Get ADC's data
           n:The channel of ADC(0~7)
           return: data of ADC[n]
        """
        return int(self.AIN[n].attrs["raw"].value)

def main():
    d = JHD1802()
    AIN = ADC()
    while True:
        disp = ""
        for i in range(6):
            x = AIN.get(i)
            print('%04d  ' % (x), end='') # Print all 8 values
            disp += '%04d ' % (x)
            if i == 2:
                disp += '\n'  # Put last 3 values on second line
        print('\r', end='')
        d.SetText(disp)     # Display the values
        time.sleep(0.1)

if __name__ == "__main__":
    main()