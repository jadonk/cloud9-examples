#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
import time
import subprocess
import os
import sys
import wave
import pyaudio
from tqdm import tqdm
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
class HCSR04:
    def __init__(self):
        try:
            self.hcsr04_Install = 0
            if not os.path.exists('/proc/device-tree/hcsr04_1057@20'):
                subprocess.call(['sudo', 'mkdir', '-p',
                    '/sys/kernel/config/device-tree/overlays/BB-GPIO-HCSR04'])
                subprocess.call(['sudo', 'dd',
                    'of=/sys/kernel/config/device-tree/overlays/BB-GPIO-HCSR04/dtbo',
                    'if=/lib/firmware/BB-GPIO-HCSR04.dtbo'])
                while not os.path.exists('/proc/device-tree/hcsr04_1057@20'):
                    time.sleep(0.1)
            self.contexts = iio.scan_contexts()
            self.ctx = iio.Context("local:")
            for dev in self.ctx.devices:
                if dev.name == "hcsr04_1057@20":
                    self.hcsr04_Install = 0
                    break
                else :
                    self.hcsr04_Install = 1
            if self.hcsr04_Install:        
                mod_path = '/lib/modules/'+GetCmdReturn('uname -r')+'/extra/seeed/hcsr04.ko'
                subprocess.call(['sudo', 'insmod', mod_path]) 
                # while len(self.ctx.devices) != 2:
                    # time.sleep(0.1)        
            self.dev = self.ctx.find_device("hcsr04_1057@20")
            GetCmdReturn('sudo config-pin P1_31 gpio')  
            
        except IOError as err:
            print("File Error:"+str(err))
            print("maybe you should reinstall the driver of hcsr04")       
         
    def GetDistance(self):
            try:
                self.dev.find_channel("distance", False)
            except AttributeError as err:
                print("maybe you should reinstall the driver of hcsr04")
                exit(1)
            return int(self.dev.find_channel("distance", False).attrs["input"].value)
class JHD1802:
    def __init__(self):
        try:
            if not os.path.exists('/proc/device-tree/aliases/jhd1802'):
                subprocess.call(['sudo', 'mkdir', '-p',
                    '/sys/kernel/config/device-tree/overlays/BB-I2C1-JHD1802'])
                subprocess.call(['sudo', 'dd',
                    'of=/sys/kernel/config/device-tree/overlays/BB-I2C1-JHD1802/dtbo',
                    'if=/lib/firmware/BB-I2C1-JHD1802.dtbo'])
                while not os.path.exists('/proc/device-tree/aliases/jhd1802'):
                    time.sleep(0.1)
            if not os.path.exists('/dev/lcd0'):
                mod_path = '/lib/modules/'+GetCmdReturn('uname -r')+'/extra/seeed/hd44780.ko'
                subprocess.call(['sudo', 'insmod', mod_path])             
                while not os.path.exists('/dev/lcd0'):
                    time.sleep(0.1)
                    
            try:
                self.f = open('/dev/lcd0', 'w')
            except IOError as err:
                subprocess.call(['sudo', 'chmod', '777', '/dev/lcd0'])
                self.f = open('/dev/lcd0', 'w')
            self.f.write('\x1b[2J')
            self.f.write('\x1b[H')
            self.f.write('seeed studio')
            self.f.flush()
        except IOError as err:
            print("File Error:"+str(err))
            print("maybe you should reinstall the driver of lcd0")
            
    def SetText(self, text):
        try:
            self.f.write('\x1b[2J')
            self.f.write('\x1b[H')
            self.f.write('%s'%text)
            self.f.flush()
            
        except IOError as err:
            print("File Error:"+str(err))
            print("maybe you should reinstall the driver of lcd0")

def main():
    Distance = HCSR04()
    Lcd = JHD1802()
    while True:
        distance = Distance.GetDistance()
        Lcd.SetText("The Distance: \r\n{} cm".format(distance))
        print("Distance is %3d \r" %distance, end = '')
        if distance < 240:
            Play_Music("/home/debian/scale/%s"%_SCALE_DEFS[distance//40])
        time.sleep(1)

if __name__ == "__main__":
    main()