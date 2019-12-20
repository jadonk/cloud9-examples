#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
import iio
import time
import sys
import subprocess
import os

class ADC:
    def __init__(self):
        self.AIN = []
        self.contexts = iio.scan_contexts()
        self.ctx = iio.Context("local:")
        self.dev = self.ctx.find_device("44e0d000.tscadc:adc.0.auto")
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
                time.sleep(0.1)
            if not os.path.exists('/dev/p981x0'):
                subprocess.call(['sudo', 'modprobe', 'p9813'])
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
    LED = RGBLed(1)
    while True:
        Sound_Data = AIN.get(0)
        Rotary_Angle_Data = AIN.get(5)
        Sound_Data = int(int(Sound_Data)/1800*255)
        Rotary_Angle_Data = int(int(Rotary_Angle_Data)/3300*255)
        if Rotary_Angle_Data > 255:
            Rotary_Angle_Data = 255
        if Sound_Data > 255 :
            Sound_Data = 255
        print("Sound_Data is %3d   Rotary_Angle_Data is %3d  \r" %
            (Sound_Data, Rotary_Angle_Data), end = '')
        LED.set(0,Rotary_Angle_Data,Sound_Data,0)
        time.sleep(0.1)

if __name__ == "__main__":
    main()