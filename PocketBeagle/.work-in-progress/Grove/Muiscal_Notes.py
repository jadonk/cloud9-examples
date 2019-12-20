#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
import time
import sys
import iio
import os
import subprocess
import pyaudio
import wave
from tqdm import tqdm

_SCALE_DEFS = [
   'do.wav',
   're.wav',
   'me.wav',
   'fa.wav',
   'so.wav',
   'la.wav',
   'ti.wav'
   ]

class LCD:
    def __init__(self):
        try:
            if not os.path.exists('/proc/device-tree/p981x_1057@20'):
                # sudo mkdir /sys/kernel/config/device-tree/overlays/BB-I2C1-JHD1802
                subprocess.call(['sudo', 'mkdir',
                    '/sys/kernel/config/device-tree/overlays/BB-I2C1-JHD1802'])
                # sudo dd if=/lib/firmware/BB-I2C1-JHD1802.dtbo \
                #     of=/sys/kernel/config/device-tree/overlays/BB-I2C1-JHD1802/dtbo \
                subprocess.call(['sudo', 'dd', 
                    'if=/lib/firmware/BB-I2C1-JHD1802.dtbo',
                    'of=/sys/kernel/config/device-tree/overlays/BB-I2C1-JHD1802/dtbo'])
                time.sleep(0.1)
            if not os.path.exists('/dev/lcd0'):
                subprocess.call(['sudo', 'modprobe', 'hd44780'])
                time.sleep(0.1)
            self.f = open('/dev/lcd0', 'w')
            self.f.write('\x1b[2J')
            self.f.write('\x1b[H')
            self.f.flush()
        except IOError as err:
            print("File Error:"+str(err))
            print("maybe you should reinstall the driver of hd44780")
    
    def set(self, text):
        return
        try:
            self.f.write('\x1b[2J')
            self.f.write('\x1b[H')
            self.f.flush()
            self.f.write('%s'%text)
            self.f.flush()
            time.sleep(.1)
        except IOError as err:
            print("File Error:"+str(err))
            print("maybe you should reinstall the driver of hd44780")
        
class Distance:
    def __init__(self):
        try:
            # echo gpio > /sys/devices/platform/ocp/ocp\:P1_31_pinmux/state
            mux = open('/sys/devices/platform/ocp/ocp:P1_31_pinmux/state', "w")
            mux.write("gpio")
            mux.close()
            if not os.path.exists('/proc/device-tree/hcsr04_1057@20'):
                # sudo mkdir /sys/kernel/config/device-tree/overlays/BB-GPIO-HCSR04
                subprocess.call(['sudo', 'mkdir',
                    '/sys/kernel/config/device-tree/overlays/BB-GPIO-HCSR04'])
                # sudo dd if=/lib/firmware/BB-GPIO-HCSR04.dtbo \
                #     of=/sys/kernel/config/device-tree/overlays/BB-GPIO-HCSR04/dtbo
                subprocess.call(['sudo', 'dd', 
                    'if=/lib/firmware/BB-GPIO-HCSR04.dtbo',
                    'of=/sys/kernel/config/device-tree/overlays/BB-GPIO-HCSR04/dtbo'])
                time.sleep(0.1)
            self.contexts = iio.scan_contexts()
            self.ctx = iio.Context("local:")
            self.dev = self.ctx.find_device("hcsr04_1057@20")
            self.chan = self.dev.find_channel("distance", False)
        except IOError as err:
            print("File Error:"+str(err))
            print("maybe you should reinstall the driver of hdd4780")
    def get(self):
        return int(self.chan.attrs["input"].value)

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
    for d in tqdm(datas):
        stream.write(d)
    # stop stream
    stream.stop_stream()
    stream.close()

    # close PyAudio
    p.terminate()
    
def main():
    l = LCD()
    d = Distance()
    while True:
        distance = d.get()
        l.set("The Distance: \r\n{} cm".format(distance))
        print(str(distance) + "    \r", end = '')
        #if int(distance) < 70:
        #    Play_Music("/tmp/scale/%s"%_SCALE_DEFS[int(int(distance)/10)])
        time.sleep(.5)

if __name__ == "__main__":
    main()