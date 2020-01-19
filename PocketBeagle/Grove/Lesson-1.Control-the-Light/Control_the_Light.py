#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
import time
import subprocess
import os
import sys
try:
    import iio
except:
    # By default the iio python bindings are not in path
    sys.path.append('/usr/lib/python2.7/site-packages/')
    import iio
    
def GetKernelVision():
    r = os.popen('uname -r')
    text = r.read() 
    r.close()
    return text.strip('\n')
class ADC:
    def __init__(self):
        self.AIN = []
        self.contexts = iio.scan_contexts()
        self.ctx = iio.Context("local:")
        for dev in self.ctx.devices:
            if 'adc.0.auto' in dev.name:
                self.name = dev.name
        self.dev = self.ctx.find_device(self.name)
        if not self.dev:
            print("maybe you should reinstall the driver of ADC")
            return
        self.AIN.append(self.dev.find_channel("voltage0", False))
        self.AIN.append(self.dev.find_channel("voltage1", False))
        self.AIN.append(self.dev.find_channel("voltage2", False))
        self.AIN.append(self.dev.find_channel("voltage3", False))
        self.AIN.append(self.dev.find_channel("voltage4", False))
        self.AIN.append(self.dev.find_channel("voltage5", False))
        self.AIN.append(self.dev.find_channel("voltage6", False))
        self.AIN.append(self.dev.find_channel("voltage7", False))
    def get(self, n):
        return int(self.AIN[n].attrs["raw"].value)

class RGBLed:
    def __init__(self, leds):
        try:
            if not os.path.exists('/proc/device-tree/p981x_1057@20'):
                subprocess.call(['sudo', 'mkdir', '-p',
                    '/sys/kernel/config/device-tree/overlays/BB-GPIO-P9813'])
                subprocess.call(['sudo', 'dd',
                    'of=/sys/kernel/config/device-tree/overlays/BB-GPIO-P9813/dtbo',
                    'if=/lib/firmware/BB-GPIO-P9813.dtbo'])
                while not os.path.exists('/proc/device-tree/p981x_1057@20'):
                    time.sleep(0.1)
            if not os.path.exists('/dev/p981x0'):
                mod_path = '/lib/modules/'+GetKernelVision()+'/extra/seeed/p9813.ko'
                subprocess.call(['sudo', 'insmod', mod_path])             
                while not os.path.exists('/dev/p981x0'):
                    time.sleep(0.1)
            self.f = open('/dev/p981x0', 'w')
            self.f.write('N %d\n'%leds)
            self.f.flush()
        except IOError as err:
            print("File Error:"+str(err))
            print("maybe you should reinstall the driver of p981x")

    def set(self, led, red, green, blue):
        try:
            self.f.write('D %d %d %d %d\n'%(led,red,green,blue))
            self.f.flush()
        except IOError as err:
            print("File Error:"+str(err))
            print("maybe you should reinstall the driver of p981x")

def main():
    AIN = ADC()
    LED = RGBLed(2)
    while True:
        Rainbow = [[1,0,0],[1,0.5,0],[1,1,0],[0,1,0],[0,1,1],[0,0,1],[1,0,1]]
        Slide_Potentiometer_Data = AIN.get(0)
        Rotary_Angle_Data = AIN.get(5)
        Slide_Potentiometer_Data = int(int(Slide_Potentiometer_Data)/3800*255)
        Rotary_Angle_Data = int(int(Rotary_Angle_Data)/3800*255)
        if Rotary_Angle_Data > 240:
            Rotary_Angle_Data = 240
        if Slide_Potentiometer_Data > 255 :
            Slide_Potentiometer_Data = 255
        print("Slide_Potentiometer_Data is %3d   Rotary_Angle_Data is %3d  \r" %
            (Slide_Potentiometer_Data, Rotary_Angle_Data), end = '')
        Rainbow_Index = Rotary_Angle_Data//40
        for i in range(len(Rainbow[Rainbow_Index])):
            Rainbow[Rainbow_Index][i] = Rainbow[Rainbow_Index][i] * Slide_Potentiometer_Data
        LED.set(0,Rainbow[Rainbow_Index][0],Rainbow[Rainbow_Index][1],Rainbow[Rainbow_Index][2])
        LED.set(1,Rainbow[Rainbow_Index][0],Rainbow[Rainbow_Index][1],Rainbow[Rainbow_Index][2])
        time.sleep(0.1)

if __name__ == "__main__":
    main()