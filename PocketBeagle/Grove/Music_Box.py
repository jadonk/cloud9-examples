#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# [Grove - 3 Axis Digital Accelerometer]
# (http://wiki.seeedstudio.com/Grove-3-Axis_Digital_Accelerometer-16g/) on I2C2
# [Grove - Speaker Plus](http://wiki.seeedstudio.com/Grove-Speaker/) on UART2
# [Grove - Chainable RGB LED X 2](http://wiki.seeedstudio.com/Grove-Chainable_RGB_LED/)
# on A2
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
def FunTimer():
    """Make the LED will shine like rainbow color"""
    Rainbow = [[255,0,0],[255,126,0],[255,255,0],[0,255,0],[0,255,255]\
    ,[0,0,255],[255,0,255]]
    global RainbowIndex
    global RainbowFlash
    if RainbowFlash:
        RainbowIndex = RainbowIndex + 1 
        if RainbowIndex > 6 :
            RainbowIndex = 0
        LED.set(0,Rainbow[RainbowIndex][0],Rainbow\
        [RainbowIndex][1],Rainbow[RainbowIndex][2])
        LED.set(1,Rainbow[RainbowIndex][0],Rainbow\
        [RainbowIndex][1],Rainbow[RainbowIndex][2])
    else:
        RainbowIndex = 0
    global timer
    timer = threading.Timer(0.5, FunTimer)
    timer.start() 
def Play_Music(file):
    """Play WAV format music
        file:the Wav format music
    """
    # end the timer
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
    # append data to datas 
    datas = []
    while len(data) > 0:
        data = f.readframes(chunk)
        datas.append(data)
    time = 0
    # play datas and display the progress bar of the music
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
    # start the timer
    timer = threading.Timer(0.5, FunTimer)
    timer.start()     
def main():
    Adx134x = ADX134X()
    global LED
    LED = P981X()
    global RainbowFlash
    RainbowFlash = False
    global RainbowIndex
    RainbowIndex = 0
    GetAttitude = 0 
    # Create timer thread that weak up after 0.5s 
    # The timer will execute the FunTimer after 0.5s    
    global timer
    timer = threading.Timer(0.5, FunTimer)
    timer.start() 
    time.sleep(1)
    while True:
        GetAttitudeLast = GetAttitude
        GetAttitude = Adx134x.MotionDetection()
        # the LED will shine like rainbow color if GetAttitude = 4 
        if GetAttitude == 4:
            RainbowFlash = True
        else:
            RainbowFlash = False
            LED.set(0,(GetAttitude&0x01)*255,(GetAttitude\
            &0x02)*255,(GetAttitude&0x04)*255)
            LED.set(1,(GetAttitude&0x01)*255,(GetAttitude\
            &0x02)*255,(GetAttitude&0x04)*255)
        # the Speaker will play music when the Attitude changed.
        if GetAttitudeLast != GetAttitude and GetAttitude != 0:
            Play_Music("/tmp/scale/%s"%_SCALE_DEFS[GetAttitude])
        time.sleep(0.05)        
if __name__ == "__main__":
    from os import path
    if not path.exists("/tmp/scale/"):
        print("Please run ./ToneGenerator.py")
        exit()
    main()