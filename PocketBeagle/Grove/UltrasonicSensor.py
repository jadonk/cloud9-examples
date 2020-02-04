#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# [Grove - Ultrasonic Distance Sensor](http://wiki.seeedstudio.com/Grove-Ultrasonic_Ranger/) on A0
import iio
import time
from Shell import GetCmdReturn,os

class HCSR04:
    def __init__(self):
        try:
            p1_31_pinmux = open('/sys/devices/platform/ocp/ocp:P1_31_pinmux/state', 'w')
            print('gpio', file=p1_31_pinmux)
            p1_31_pinmux.close()
            if not os.path.exists('/proc/device-tree/hcsr04_1057@20'):
                GetCmdReturn('sudo mkdir -p \
                /sys/kernel/config/device-tree/overlays/BB-GPIO-HCSR04')                  
                GetCmdReturn('sudo dd \
                of=/sys/kernel/config/device-tree/overlays/BB-GPIO-HCSR04/dtbo \
                if=/lib/firmware/BB-GPIO-HCSR04.dtbo')                    
                while not os.path.exists('/proc/device-tree/hcsr04_1057@20'):
                    time.sleep(0.1)    
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
            return int(self.dev.find_channel("distance", False).attrs["input"].value)
def main():
    Distance = HCSR04()
    while True:
        print('The Distance is:%d'%(Distance.GetDistance()), end = '        \r')
        time.sleep(0.5)

if __name__ == "__main__":
    main()            