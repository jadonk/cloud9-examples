# Copyright (c) 2020 SeeedStudio
# Author: Hansen Chen
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# [Grove - Ultrasonic Distance Sensor](http://wiki.seeedstudio.com/Grove-Ultrasonic_Ranger/) on A0
import iio
import time
from Shell import GetCmdReturn,os

class HCSR04:
    """HCSR04 Ultrasonic distance sensor"""
    def __init__(self):
        """Initialize the HCSR04 using iio python library
        """    
        try:
            # Config p1_31 to GPIO mode
            p1_31_pinmux = open('/sys/devices/platform/ocp/ocp:P1_31_pinmux/state', 'w')
            print('gpio', file=p1_31_pinmux)
            p1_31_pinmux.close()
            
            # Check BB-GPIO-HCSR04 whether install successfully
            # if not reinstall it            
            if not os.path.exists('/proc/device-tree/hcsr04_1057@20'):
                GetCmdReturn('sudo mkdir -p \
                /sys/kernel/config/device-tree/overlays/BB-GPIO-HCSR04')                  
                GetCmdReturn('sudo dd \
                of=/sys/kernel/config/device-tree/overlays/BB-GPIO-HCSR04/dtbo \
                if=/lib/firmware/BB-GPIO-HCSR04.dtbo')                    
                while not os.path.exists('/proc/device-tree/hcsr04_1057@20'):
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