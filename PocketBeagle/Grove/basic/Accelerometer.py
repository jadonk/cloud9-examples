#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# [Grove - 3 Axis Digital Accelerometer]
# (http://wiki.seeedstudio.com/Grove-3-Axis_Digital_Accelerometer-16g/) on I2C2
import time
import os 
import iio
class ADX134X:
    """ADXL345 triple-axis accelerometer."""
    def __init__(self):
        """Initialize the ADXL345 accelerometer using iio python library
        """
        self._Acceleration_xyz = []
        self.Path = '/proc/device-tree/aliases/adxl345'
        try:
            # Scan the adxl345 by using IIO python library        
            self.contexts = iio.scan_contexts()
            self.ctx = iio.Context("local:") 
            self.dev = self.ctx.find_device("adxl345")
            # Initialize the data of adxl345 for SlidingAverage function
            self._Acceleration_xyz.append(self.dev.find_channel("accel_x", False))
            self._Acceleration_xyz.append(self.dev.find_channel("accel_y", False))
            self._Acceleration_xyz.append(self.dev.find_channel("accel_z", False))
        except IOError as err:
            print("File Error:"+str(err))
            print("maybe you should reinstall the driver of adxl345")       

    def xyzRead(self): 
        """ Simple gesture detection for adxl345 
            return: x, y, z acceleration  
        """
        #Return xyz data of adxl345
        x = int(self._Acceleration_xyz[0].attrs["raw"].value)
        y = int(self._Acceleration_xyz[1].attrs["raw"].value)
        z = int(self._Acceleration_xyz[2].attrs["raw"].value)       
        return [x,y,z]
                           
def main():
    Adx134x = ADX134X()
    while True:
        print(Adx134x.xyzRead(),end= '        \r')
        time.sleep(0.5)
if __name__ == "__main__":
    main()