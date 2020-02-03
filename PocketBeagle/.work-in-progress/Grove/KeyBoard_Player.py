#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# [Grove - 12 Key Capacitive I2C Touch Sensor V2](http://wiki.seeedstudio.com/Grove-12_Key_Capacitive_I2C_Touch_Sensor_V2-MPR121/) on I2C2
# [Grove – Speaker](http://wiki.seeedstudio.com/Grove-Speaker/) on UART2
import time
import wave
import os
import pyaudio
from tqdm import tqdm
CHANNEL_NUM                               = 12
ResultStr = [1, 1, 1]
_SCALE_DEFS = [
   'do.wav',
   're.wav',
   'me.wav',
   'fa.wav',
   'so.wav',
   'la.wav',
   'ti.wav',
   'do+.wav'
   ]
def Play_Music(file):
    global Mpr121
    Mpr121Data = [0]*2
    # define stream chunk 
    chunk = 1024
    # open a wav format music
    f = wave.open(file,"rb")
    # instantiate PyAudio
    p = pyaudio.PyAudio()
    # open stream
    def callback(in_data, frame_count, time_info, status):
        global Mpr121Data 
        data = f.readframes(frame_count)
        if Mpr121Data[0] != 0:
            return (data,pyaudio.paContinue)
        return (data,pyaudio.paComplete)
    stream = p.open(format = p.get_format_from_width(f.getsampwidth()),
                                channels = f.getnchannels(),
                                rate = f.getframerate(),
                                output = True,
                                stream_callback=callback)
    stream.start_stream()
    
    while stream.is_active():
        Mpr121Data = Mpr121.get()
        time.sleep(0.01)  

    # stop stream
    stream.stop_stream()
    stream.close()
    f.close()
    # close PyAudio
    p.terminate()
    
class MPR121:
    def __init__(self):
        try:
            if not os.path.exists('/proc/device-tree/aliases/mpr121'):
                subprocess.call(['sudo', 'mkdir', '-p',
                    '/sys/kernel/config/device-tree/overlays/BB-I2C2-MPR121'])
                subprocess.call(['sudo', 'dd',
                    'of=/sys/kernel/config/device-tree/overlays/BB-I2C2-MPR121/dtbo',
                    'if=/lib/firmware/BB-I2C2-MPR121.dtbo'])
                time.sleep(0.1)
            if not os.path.exists('/sys/devices/platform/ocp/4819c000.i2c/i2c-2/2-005b/mpr121_data'):
                subprocess.call(['sudo', 'modprobe', 'hd44780'])
                time.sleep(0.1)
            try:
                self.f = open('/sys/devices/platform/ocp/4819c000.i2c/i2c-2/2-005b/mpr121_data', 'r')
            except IOError as err:
                subprocess.call(['sudo', 'chmod', '777',
                    '/sys/devices/platform/ocp/4819c000.i2c/i2c-2/2-005b/mpr121_data'])
                self.f = open('/sys/devices/platform/ocp/4819c000.i2c/i2c-2/2-005b/mpr121_data', 'r')
        except IOError as err:
            print("File Error:"+str(err))
            print("maybe you should reinstall the driver of mpr121")
    def ParseAndPrintResult(self, result):
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
                        print("Channel %d is pressed"%i)
                else:
                    if(1 == touch_flag[i]):
                        touch_flag[i] = 0
                        print("Channel %d is released"%i)
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
        return [value, self.ParseAndPrintResult(value)]
Mpr121 = MPR121()
def main():
    
    while True:
        GetMpr121 = Mpr121.get()
        Mpr121Result = GetMpr121[1]
        if any(Mpr121Result) != False:
            for i in range(CHANNEL_NUM):
                if(Mpr121Result[i] == 1):
                    if i > 3 :
                        Play_Music("/home/debian/scale/%s"%_SCALE_DEFS[i-4])
                    else :
                        Play_Music("/home/debian/scale/%s"%_SCALE_DEFS[i])
        time.sleep(0.05)
if __name__ == "__main__":
    main()