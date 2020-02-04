#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# [Grove - 12 Key Capacitive I2C Touch Sensor V2](http://wiki.seeedstudio.com/Grove-12_Key_Capacitive_I2C_Touch_Sensor_V2-MPR121/) on I2C2
import time
from Shell import GetCmdReturn,os
class MPR121:
    def __init__(self):
        try:
            if not os.path.exists('/proc/device-tree/aliases/mpr121'):
                GetCmdReturn('sudo mkdir -p \
                /sys/kernel/config/device-tree/overlays/BB-I2C2-mpr121')
                GetCmdReturn('sudo dd \
                of=/sys/kernel/config/device-tree/overlays/BB-I2C2-mpr121/dtbo \
                if=/lib/firmware/BB-I2C2-mpr121.dtbo')
                while not os.path.exists('/proc/device-tree/aliases/mpr121'):
                    time.sleep(0.1)   
            if 'mpr121' in GetCmdReturn('lsmod | grep mpr121'):
                GetCmdReturn('sudo rmmod mpr121') 
            while 'mpr121' in GetCmdReturn('lsmod | grep mpr121'):
                time.sleep(0.1)                     
            GetCmdReturn('sudo modprobe -i mpr121')
            while not 'mpr121' in GetCmdReturn('lsmod | grep mpr121'):
                time.sleep(0.1)
            if not os.path.exists('/sys/bus/i2c/drivers/mpr121/2-005b/mpr121_init'):
                if 'mpr121' in GetCmdReturn('lsmod | grep mpr121'):
                    GetCmdReturn('sudo rmmod mpr121') 
                while 'mpr121' in GetCmdReturn('lsmod | grep mpr121'):
                    time.sleep(0.1)                     
                GetCmdReturn('sudo modprobe -i mpr121')
                while not 'mpr121' in GetCmdReturn('lsmod | grep mpr121'):
                    time.sleep(0.1)               
            GetCmdReturn('sudo chmod 777\
            /sys/bus/i2c/drivers/mpr121/2-005b/mpr121_init')
            GetCmdReturn('echo 1 >\
            /sys/bus/i2c/drivers/mpr121/2-005b/mpr121_init')    
            self.f = open('/sys/devices/platform/ocp/4819c000.i2c/i2c-2/2-005b/mpr121_data', 'r')               
        except IOError as err:
            print("File Error:"+str(err))
            print("maybe you should reinstall the driver of mpr121")
    def parse_and_print_result(self, result):
        CHANNEL_NUM = 12
        ResultStr = [1, 1, 1]
        touch_flag = [0]*CHANNEL_NUM
        if result != 0:
            result = result % 1000
            ResultStr[0] = result // 100
            ResultStr[1] = result % 100 // 10
            ResultStr[2] = result % 100 % 10
            result = ResultStr[0] * (1<<8) | ResultStr[1] * (1<<4) | ResultStr[2]
            for i in range(CHANNEL_NUM):
                if(result & 1 << i):
                    if(0 == touch_flag[i]):
                        touch_flag[i] = 1
                        # print("Channel %d is pressed"%i)
                else:
                    if(1 == touch_flag[i]):
                        touch_flag[i] = 0
                        # print("Channel %d is released"%i)
        return touch_flag
    def get(self):
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
        return [value, self.parse_and_print_result(value)]

def main():
    t = MPR121()
    while True:
        print(t.get(), end = '        \r')
        time.sleep(0.05)

if __name__ == "__main__":
    main()