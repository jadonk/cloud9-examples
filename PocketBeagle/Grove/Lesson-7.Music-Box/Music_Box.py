#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# [Grove - 16x2 LCD](http://wiki.seeedstudio.com/Grove-16x2_LCD_Series/) on I2C1
# [Grove - Speaker Plus ](http://wiki.seeedstudio.com/Grove-16x2_LCD_Series/) on UART2
# [Grove - Button x 2](https://www.seeedstudio.com/Grove-Button.html) on A5 and UART4
import time
import subprocess
import os
import sys
import wave
import pyaudio
from tqdm import tqdm
import math
try:
    import iio
except:
    # By default the iio python bindings are not in path
    sys.path.append('/usr/lib/python2.7/site-packages/')
    import iio
_SCALE_DEFS = [
   'do.wav',
   're.wav',
   'me.wav',
   'fa.wav',
   'so.wav',
   'la.wav',
   'ti.wav'
   ]
def Play_Music(file):
    # define stream chunk
    chunk = 1024
    # open a wav format music
    f = wave.open(file,"rb")
    # instantiate PyAudio
    p = pyaudio.PyAudio()
    # open stream
    stream = p.open(format = p.get_format_from_width(f.getsampwidth()),
                                channels = f.getnchannels(),
                                rate = f.getframerate(),
                                output = True)
    # read data
    data = f.readframes(chunk)
    # play stream
    datas = []
    while len(data) > 0:
        data = f.readframes(chunk)
        datas.append(data)
    time = 0
    for d in tqdm(datas):
        time = time + 1
        stream.write(d)
        if time > 250:
            break
    # stop stream
    stream.stop_stream()
    stream.close()

    # close PyAudio
    p.terminate()   
def GetCmdReturn(cmd):
    r = os.popen(cmd)
    text = r.read() 
    r.close()
    return text.strip('\n')    
class ADX134X:
    
    def __init__(self):
        self._Acceleration_xyz = []
        self.data_x = [0] * 5  
        self.data_y = [0] * 5 
        self.data_z = [0] * 5
        try:
            self.Adx134xInstall = 0
            if not os.path.exists('/proc/device-tree/aliases/adxl345'):
                subprocess.call(['sudo', 'mkdir', '-p',
                    '/sys/kernel/config/device-tree/overlays/BB-I2C2-ADXL34X'])
                subprocess.call(['sudo', 'dd',
                    'of=/sys/kernel/config/device-tree/overlays/BB-I2C2-ADXL34X/dtbo',
                    'if=/lib/firmware/BB-I2C2-ADXL34X.dtbo'])
                while not os.path.exists('/proc/device-tree/aliases/adxl345'):
                    time.sleep(0.1)
            self.contexts = iio.scan_contexts()
            self.ctx = iio.Context("local:")                
            self.dev = self.ctx.find_device("adxl345")
            self._Acceleration_xyz.append(self.dev.find_channel("accel_x", False))
            self._Acceleration_xyz.append(self.dev.find_channel("accel_y", False))
            self._Acceleration_xyz.append(self.dev.find_channel("accel_z", False))
            print(self._Acceleration_xyz[0].attrs["raw"].value)
            for i in range(5):
                self.data_x[i] = int(self._Acceleration_xyz[0].attrs["raw"].value)
                self.data_y[i] = int(self._Acceleration_xyz[1].attrs["raw"].value)
                self.data_z[i] = int(self._Acceleration_xyz[2].attrs["raw"].value)
        except IOError as err:
            print("File Error:"+str(err))
            print("maybe you should reinstall the driver of adxl345")       
    def SlidingAverage(self,inputs,n,per):
        sum = 0
        inputs.remove(inputs[0])
        inputs.append(int(self._Acceleration_xyz[n].attrs["raw"].value))
        for i in range(per):
            sum = sum + inputs[i]
        return (sum // per)
    # return six side
    def MotionDetection(self): 
        data = [0]*3
        x = self.SlidingAverage(self.data_x,0,5)
        y = self.SlidingAverage(self.data_y,1,5)
        z = self.SlidingAverage(self.data_z,2,5)
        
        data[2] = math.atan2(z,math.sqrt((x*x+y*y)))
        data[0] = math.atan2(x,math.sqrt((z*z+y*y)))
        data[1] = math.atan2(y,math.sqrt((z*z+x*x)))
        
        data[2] = int(data[2] / math.pi*180)
        data[0] = int(data[0] / math.pi*180)
        data[1] = int(data[1] / math.pi*180)

        print(data)

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
        # return data            
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
                mod_path = '/lib/modules/'+GetCmdReturn('uname -r')+'/extra/seeed/p9813.ko'
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
    LED = RGBLed(2)
    Adx134x = ADX134X()
    GetAttitude = 0
    while True:
        GetAttitude_Last = GetAttitude
        GetAttitude = Adx134x.MotionDetection()
        LED.set(0,(GetAttitude&0x01)*255,(GetAttitude&0x02)*255,(GetAttitude&0x04)*255)
        LED.set(1,(GetAttitude&0x01)*255,(GetAttitude&0x02)*255,(GetAttitude&0x04)*255)
        if GetAttitude_Last != GetAttitude and GetAttitude != 0:
            Play_Music("/home/debian/scale/%s"%_SCALE_DEFS[GetAttitude])
        time.sleep(0.05)        
if __name__ == "__main__":
    main()