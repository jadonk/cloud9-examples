#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# [Grove - 16x2 LCD](http://wiki.seeedstudio.com/Grove-16x2_LCD_Series/) on I2C1
# [Grove - Speaker Plus ](http://wiki.seeedstudio.com/Grove-16x2_LCD_Series/) on UART2
# [Grove - Button x 2](https://www.seeedstudio.com/Grove-Button.html) on A5 and UART4
from evdev import InputDevice
import evdev
import time
import subprocess
import os
import sys
import wave
import pyaudio
try:
    import iio
except:
    # By default the iio python bindings are not in path
    sys.path.append('/usr/lib/python2.7/site-packages/')
    import iio
def GetCmdReturn(cmd):
    r = os.popen(cmd)
    text = r.read() 
    r.close()
    return text.strip('\n')    
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
        with open('/dev/lcd0', 'w') as f:
            f.write('\x1b[2J')
            f.write('\x1b[H')
            f.write('%s'%text)
            self.f.flush()


class BUTTON:
    def __init__(self):
        try:
            if not os.path.exists('/proc/device-tree/gpio_keys/grove_button_1057_0@0'):
                subprocess.call(['sudo', 'mkdir', '-p',
                    '/sys/kernel/config/device-tree/overlays/BB-GPIO-GROVE-BUTTON'])
                subprocess.call(['sudo', 'dd',
                    'of=/sys/kernel/config/device-tree/overlays/BB-GPIO-GROVE-BUTTON/dtbo',
                    'if=/lib/firmware/BB-GPIO-GROVE-BUTTON.dtbo'])
                while not os.path.exists('/proc/device-tree/gpio_keys/grove_button_1057_0@0'):
                    time.sleep(0.1) 
            subprocess.call(['sudo', 'config-pin','P2_35','gpio'])
            subprocess.call(['sudo', 'config-pin','P2_05','gpio'])
            GetCmdReturn('sudo chmod 777 /dev/input/event*')
            devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
            for device in devices:
                if 'gpio_keys' in device.name:
                    self.path = device.path
                    print(self.path)
            del devices
            
        except IOError as err:
            print("File Error:"+str(err))
            print("maybe you should reinstall the driver of button")       
         
    def GetKeyStatus(self):  
        try:
            self.key = InputDevice(self.path)
        except IOError as err:
            print("File Error:"+str(err))
            print("maybe you should reinstall the driver of button")
        return self.key.active_keys()
    def PlayMusic(self,file):
        # define stream chunk 
        chunk = 1024
        # open a wav format music
        f = wave.open(file,"rb")
        # instantiate PyAudio
        p = pyaudio.PyAudio()
        key = InputDevice(self.path)
        def callback(in_data, frame_count, time_info, status):
            data = f.readframes(frame_count)
            if len(key.active_keys()):
                return (data,pyaudio.paContinue)
            return (data,pyaudio.paComplete)
        # open stream
        stream = p.open(format = p.get_format_from_width(f.getsampwidth()),
                                    channels = f.getnchannels(),
                                    rate = f.getframerate(),
                                    output = True,
                                    stream_callback=callback)
        # read data
        stream.start_stream()
        while stream.is_active():
            time.sleep(0.01)  
        # stop stream
        stream.stop_stream()
        stream.close()
        # close PyAudio
        p.terminate()

def main():
    MusciIndex = 0
    files= os.listdir("/home/debian/scale")
    print(files)
    Button = BUTTON()
    Lcd = JHD1802()
    while True:
        KeyStatus = Button.GetKeyStatus()
        if(len(KeyStatus)):
            if KeyStatus[0] == 256:
                MusciIndex = MusciIndex + 1
                if MusciIndex > 6:
                    MusciIndex = 0
                Lcd.SetText("scale: \r\n{}".format(files[MusciIndex]))
                Button.PlayMusic("/home/debian/scale/%s"%files[MusciIndex])
            if KeyStatus[0] == 257:
                MusciIndex = MusciIndex - 1
                if MusciIndex < 0:
                    MusciIndex = 6
                Lcd.SetText("scale: \r\n{}".format(files[MusciIndex]))
                Button.PlayMusic("/home/debian/scale/%s"%files[MusciIndex])

        time.sleep(0.05)
if __name__ == "__main__":
    main()