#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# [Grove - 16x2 LCD](http://wiki.seeedstudio.com/Grove-16x2_LCD_Series/) on I2C1
# [Grove - Speaker Plus ](http://wiki.seeedstudio.com/Grove-16x2_LCD_Series/) on UART2
# [Grove - Button x 2](https://www.seeedstudio.com/Grove-Button.html) on A5 and UART4

import wave
import pyaudio
import os 
import time
from Button import BUTTON
from LCD import JHD1802
from Shell import GetCmdReturn,os
MusicKeyStatus = []*2
def PlayMusic(file):
    # define stream chunk 
    chunk = 512
    # open a wav format music
    f = wave.open(file,"rb")
    # instantiate PyAudio
    p = pyaudio.PyAudio()
    def callback(in_data, frame_count, time_info, status):
        # global MusicKeyStatus
        global MusicKeyStatus
        # print("Callback MusicKeyStatus: %s"%MusicKeyStatus)
        data = f.readframes(frame_count)
        if len(MusicKeyStatus):
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
        global keys
        global MusicKeyStatus
        MusicKeyStatus = keys.GetKeyStatus()
        time.sleep(0.01)  
    # stop stream
    stream.stop_stream()
    stream.close()
    # close PyAudio
    p.terminate()
    
keys = BUTTON()
def main():
    MusciIndex = 0
    if os.path.exists('/var/lib/cloud9/PocketBeagle/Grove/*.wav'): 
        GetCmdReturn('sudo mv /var/lib/cloud9/PocketBeagle/Grove/*.wav \
        /tmp/scale/')
    files= os.listdir("/tmp/scale")
    print(files)
    global keys
    Lcd = JHD1802()
    while True:
        KeyStatus = keys.GetKeyStatus()
        if(len(KeyStatus)):
            if KeyStatus[0] == 256:
                MusciIndex = MusciIndex + 1
                if MusciIndex > 6:
                    MusciIndex = 0
                Lcd.SetText("scale: \r\n{}".format(files[MusciIndex]))
                PlayMusic("/tmp/scale/%s"%files[MusciIndex])
            if KeyStatus[0] == 257:
                MusciIndex = MusciIndex - 1
                if MusciIndex < 0:
                    MusciIndex = 6
                Lcd.SetText("scale: \r\n{}".format(files[MusciIndex]))
                PlayMusic("/tmp/scale/%s"%files[MusciIndex])

        time.sleep(0.05)
if __name__ == "__main__":
    main()