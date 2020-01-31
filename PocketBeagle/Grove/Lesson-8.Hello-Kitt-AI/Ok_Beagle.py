#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# [Grove - Analog Microphone](http://wiki.seeedstudio.com/Grove-Speaker/) on PWM
# [Grove - Grove - Speaker Plus](http://wiki.seeedstudio.com/Grove-Chainable_RGB_LED/) on UART2
# [Grove - Chainable RGB LED](http://wiki.seeedstudio.com/Grove-Chainable_RGB_LED/) on A2
import time
import subprocess
import os
import sys
import signal
from snowboy import snowboydecoder

def GetCmdReturn(cmd):
    r = os.popen(cmd)
    text = r.read() 
    r.close()
    return text.strip('\n') 
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
            
interrupted = False
def signal_handler(signal, frame):
    global interrupted
    interrupted = True


def interrupt_callback():
    global interrupted
    return interrupted


# capture SIGINT signal, e.g., Ctrl+C
signal.signal(signal.SIGINT, signal_handler)

detector = snowboydecoder.HotwordDetector('/usr/lib/python3/dist-packages/snowboy/resources/models/Ok_Beagle.pmdl', sensitivity=0.5)
print('Listening... Press Ctrl+C to exit')
def callback():
    LED.set(0,255,255,0)
    LED.set(1,255,255,0)
    time.sleep(1)
    LED.set(0,0,0,0)
    LED.set(1,255,255,0)
LED = RGBLed(2)
LED.set(0,0,0,0)
LED.set(1,0,0,0)
# main loop
detector.start(detected_callback=callback,
               interrupt_check=interrupt_callback,
               sleep_time=0.03)

detector.terminate()
