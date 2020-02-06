#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# [Grove - Ultrasonic Distance Sensor](http://wiki.seeedstudio.com/Grove-Ultrasonic_Ranger/) on A0
import iio
import time
from Shell import ConfigGPIO,InstallDTBO
import os
class HCSR04:
    """HCSR04 Ultrasonic distance sensor"""
    def __init__(self):
        """Initialize the HCSR04 using iio python library
        """    
        self.Path = '/proc/device-tree/hcsr04_1057@20'
        try:
            # Config P1_31 to GPIO mode
            ConfigGPIO('P1_31')
            # Check BB-GPIO-HCSR04 whether install successfully
            # if not reinstall it            
            if not os.path.exists(self.Path):
                InstallDTBO('BB-GPIO-P9813')                
                while not os.path.exists(self.Path):
                    time.sleep(0.1)   
            # Scan the adxl345 by using IIO python library        
            self.contexts = iio.scan_contexts()
            self.ctx = iio.Context("local:")                    
            self.dev = self.ctx.find_device("hcsr04_1057@20")
            if not self.dev:
                print("maybe you should reinstall the driver of hcsr")
                return
        except IOError as err:
            print("File Error:"+str(err))
            print("maybe you should reinstall the driver of hcsr04")       
    def GetDistance(self):
        """Get the GetDistance using IIO python library
        """
        return int(self.dev.find_channel("distance", False).attrs["input"].value)
def main():
    Distance = HCSR04()
    while True:
        print('The Distance is:%d'%(Distance.GetDistance()), end = '        \r')
        time.sleep(0.5)
if __name__ == "__main__":
    main()