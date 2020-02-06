#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# [Grove - 12 Key Capacitive I2C Touch Sensor V2](http://wiki.seeedstudio.com/Grove-12_Key_Capacitive_I2C_Touch_Sensor_V2-MPR121/) on I2C2
import time
from Shell import ReinstallModule,InstallDTBO,GetCmdReturn
import os 
class MPR121:
    """MPR121 12 Key Capacitive I2C Touch Sensor"""
    def __init__(self):
        """Initialize the MPR121 using file python library"""
        try:
            # Check BB-I2C2-mpr121 whether install successfully
            # if not reinstall it             
            if not os.path.exists('/proc/device-tree/aliases/mpr121'):
                InstallDTBO('BB-I2C2-mpr121')
                while not os.path.exists('/proc/device-tree/aliases/mpr121'):
                    time.sleep(0.1)  
            #Reinstall mpr121 module to support hot plug        
            ReinstallModule('mpr121')
            if not os.path.exists('/sys/bus/i2c/drivers/mpr121/2-005b/mpr121_init'):
                ReinstallModule('mpr121') 
            #Enable mpr121
            GetCmdReturn('sudo chmod 777\
            /sys/bus/i2c/drivers/mpr121/2-005b/mpr121_init')
            GetCmdReturn('echo 1 >\
            /sys/bus/i2c/drivers/mpr121/2-005b/mpr121_init') 
            #Open the mpr121_data using file python library
            self.f = open('/sys/devices/platform/ocp/4819c000.i2c/i2c-2/2-005b/mpr121_data', 'r')   
        except IOError as err:
            print("File Error:"+str(err))
            print("maybe you should reinstall the driver of mpr121")
    def parse_and_print_Input(self,Input):
        """Parse the raw data form MPR121 to List 
        that describes which one is touched on 
        12 Key Capacitive I2C Touch Sensor.
        Input:raw data form MPR121
        return:List that describes which one is touched on 
        12 Key Capacitive I2C Touch Sensor.
        """
        CHANNEL_NUM = 12
        InputStr = [1, 1, 1]
        TouchValue = [0]*CHANNEL_NUM
        #Parse the raw data form MPR121 to List,if MPR121 is touched.       
        if Input != 0:
            # Set raw data to decimal 
            Input = Input % 1000
            InputStr[0] = Input // 100
            InputStr[1] = Input % 100 // 10
            InputStr[2] = Input % 100 % 10
            Input = InputStr[0] * (1<<8) | InputStr[1] * (1<<4) | InputStr[2]
            # Set to decimal to List
            for i in range(CHANNEL_NUM):
                if(Input & 1 << i):
                    if(0 == TouchValue[i]):
                        TouchValue[i] = 1
                else:
                    if(1 == TouchValue[i]):
                        TouchValue[i] = 0
        return TouchValue
    def get(self):
        """Get the raw data form MPR121
        return:Raw data form MPR121
        """
        value = 0
        try:
            self.f.seek(0)
            text = self.f.readlines()
            try:
                if(len(text)>=1):
                    value = int(text[0].strip('\n'))
            except IndexError as err:
                print("Bug!")
            except ValueError as err:
                print("Multi-touch is not supported")
        except IOError as err:
            print("File Error:"+str(err))
            print("maybe you should reinstall the driver of mpr121")
        return [value, self.parse_and_print_Input(value)]
def main():
    t = MPR121()
    while True:
        print(t.get(), end = '        \r')
        time.sleep(0.05)
if __name__ == "__main__":
    main()