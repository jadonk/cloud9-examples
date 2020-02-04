#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# [Grove - 3 Axis Digital Accelerometer](http://wiki.seeedstudio.com/Grove-3-Axis_Digital_Accelerometer-16g/) on I2C2
# [Grove - Speaker Plus](http://wiki.seeedstudio.com/Grove-Speaker/) on UART2
# [Grove - Chainable RGB LED X 2](http://wiki.seeedstudio.com/Grove-Chainable_RGB_LED/) on A2
import time
import wave
import pyaudio
from tqdm import tqdm
import math
import threading
from RGBLed import P981X
from Accelerometer import ADX134X
_SCALE_DEFS = [
   'do.wav',
   're.wav',
   'me.wav',
   'fa.wav',
   'so.wav',
   'la.wav',
   'ti.wav'
   ]
Rainbow_Index = 0
Rainbow_Flash = False

def fun_timer():
    Rainbow = [[255,0,0],[255,126,0],[255,255,0],[0,255,0],[0,255,255],[0,0,255],[255,0,255]]
    global Rainbow_Index
    global Rainbow_Flash
    global LED
    if Rainbow_Flash:
        Rainbow_Index = Rainbow_Index + 1 
        if Rainbow_Index > 6 :
            Rainbow_Index = 0
        LED.set(0,Rainbow[Rainbow_Index][0],Rainbow[Rainbow_Index][1],Rainbow[Rainbow_Index][2])
        LED.set(1,Rainbow[Rainbow_Index][0],Rainbow[Rainbow_Index][1],Rainbow[Rainbow_Index][2])
    else:
        Rainbow_Index = 0
    global timer
    timer = threading.Timer(0.5, fun_timer)
    timer.start() 

def Play_Music(file):
    global timer
    timer.cancel()
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
        if time > len(datas)//10:
            break
    # stop stream
    stream.stop_stream()
    stream.close()

    # close PyAudio
    p.terminate()   
    
    timer = threading.Timer(0.5, fun_timer)
    timer.start()     
LED = P981X()
def main():
    Adx134x = ADX134X()
    global LED
    global Rainbow_Flash
    GetAttitude = 0 
    timer = threading.Timer(0.5, fun_timer)
    timer.start() 
    time.sleep(1)
    while True:
        GetAttitude_Last = GetAttitude
        GetAttitude = Adx134x.MotionDetection()
        if GetAttitude == 4:
            Rainbow_Flash = True
        else:
            Rainbow_Flash = False
            LED.set(0,(GetAttitude&0x01)*255,(GetAttitude&0x02)*255,(GetAttitude&0x04)*255)
            LED.set(1,(GetAttitude&0x01)*255,(GetAttitude&0x02)*255,(GetAttitude&0x04)*255)
        if GetAttitude_Last != GetAttitude and GetAttitude != 0:
            Play_Music("/tmp/scale/%s"%_SCALE_DEFS[GetAttitude])
        time.sleep(0.05)        
if __name__ == "__main__":
    main()