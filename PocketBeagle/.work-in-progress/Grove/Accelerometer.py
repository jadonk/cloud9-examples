#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# [Grove - 3 Axis Digital Accelerometer](http://wiki.seeedstudio.com/Grove-3-Axis_Digital_Accelerometer-16g/) on I2C2
import time
from Shell import ReinstallModule,InstallDTBO
import os 
import iio
import math
class ADX134X:
    """ADXL345 triple-axis accelerometer."""
    def __init__(self):
        """Initialize the ADXL345 accelerometer using iio python library
        """
        self._Acceleration_xyz = []
        self.data_x = [0] * 5   
        self.data_y = [0] * 5 
        self.data_z = [0] * 5
        try:
            # Check BB-I2C2-ADXL34X whether install successfully
            # if not reinstall it
            if not os.path.exists('/proc/device-tree/aliases/adxl345'):
                InstallDTBO('BB-I2C2-ADXL34X')
                while not os.path.exists('/proc/device-tree/aliases/adxl345'):
                    time.sleep(0.1) 
            #  Reinstall adxl345_xxx module to support hot plug                   
            ReinstallModule('adxl345_i2c')    
            # Scan the adxl345 by using IIO python library        
            self.contexts = iio.scan_contexts()
            self.ctx = iio.Context("local:") 
            self.dev = self.ctx.find_device("adxl345")
            # Initialize the data of adxl345 for SlidingAverage function
            self._Acceleration_xyz.append(self.dev.find_channel("accel_x", False))
            self._Acceleration_xyz.append(self.dev.find_channel("accel_y", False))
            self._Acceleration_xyz.append(self.dev.find_channel("accel_z", False))
            for i in range(5):
                self.data_x[i] = int(self._Acceleration_xyz[0].attrs["raw"].value)
                self.data_y[i] = int(self._Acceleration_xyz[1].attrs["raw"].value)
                self.data_z[i] = int(self._Acceleration_xyz[2].attrs["raw"].value)                
        except IOError as err:
            print("File Error:"+str(err))
            print("maybe you should reinstall the driver of adxl345")       
    def SlidingAverage(self,inputs,n,per):
        """Sliding filter algorithm for adxl345 to make data smooth
            inputs:raw data of adxl345
            n:The axis of adxl345(0 = X 1 = Y 2 = Z) 
            per:The times of Sliding
            return:data that more than raw data smooth
        """    
        sum = 0
        # Slide data to out 
        inputs.remove(inputs[0])
        # Slide data to in 
        inputs.append(int(self._Acceleration_xyz[n].attrs["raw"].value))
        # Get average 
        for i in range(per):
            sum = sum + inputs[i]
        return (sum // per)
    def MotionDetection(self): 
        """ Simple gesture detection for adxl345 
            return: Which of the six sides is adxl345 on   
        """
        data = [0]*3
        #Make data of adxl345 smooth
        x = self.SlidingAverage(self.data_x,0,5)
        y = self.SlidingAverage(self.data_y,1,5)
        z = self.SlidingAverage(self.data_z,2,5)        
        #Set data to angle  
        data[2] = math.atan2(z,math.sqrt((x*x+y*y)))
        data[0] = math.atan2(x,math.sqrt((z*z+y*y)))
        data[1] = math.atan2(y,math.sqrt((z*z+x*x)))        
        data[2] = int(data[2] / math.pi*180)
        data[0] = int(data[0] / math.pi*180)
        data[1] = int(data[1] / math.pi*180)
        print(data)        
        # Get which one of six sides        
        if abs(data[2] - 90) < 10:
            return 1
        elif abs(data[2] - 90) > 165 :
            return 4
        elif abs(data[0] - 90) < 10:
            return 2
        elif abs(data[0] - 90) > 170 :
            return 5
        elif abs(data[1] - 90) < 10:
            return 3
        elif abs(data[1] - 90) > 175:
            return 6
        else :
            return 0                            
def main():
    Adx134x = ADX134X()
    while True:
        print(Adx134x.MotionDetection(),end= '        \r')
        time.sleep(0.5)
if __name__ == "__main__":
    main()