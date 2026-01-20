#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# [Grove - 16x2 LCD](http://wiki.seeedstudio.com/Grove-16x2_LCD_Series/) on I2C1
# [Grove - Speaker Plus ](http://wiki.seeedstudio.com/Grove-16x2_LCD_Series/) on UART2
# [Grove - Button x 2](https://www.seeedstudio.com/Grove-Button.html) on A5 and UART4
import wave
import pyaudio
import os 
import time
import threading
from Button import BUTTON
from LCD import JHD1802
from Shell import GetCmdReturn
def FunTimer():
    """Update the LCD every 0.25 seconds"""
    global MusciIndex
    global files
    Lcd.SetText("scale: \r\n{}".format(files[MusciIndex]))
    global timer
    timer = threading.Timer(0.25, FunTimer)
    timer.start()
def PlayMusic(file):
    """Play WAV format music when the Button is pressed 
        file:the Wav format music
    """
    # define stream chunk 
    chunk = 512
    # open a wav format music
    f = wave.open(file,"rb")
    # instantiate PyAudio
    p = pyaudio.PyAudio()
    #define callback function
    def callback(in_data, frame_count, time_info, status):
        data = f.readframes(frame_count)
        #the function will return pyaudio.paContinue when the Button is pressed 
        if len(MusicKeyStatus):
            return (data,pyaudio.paContinue)
        return (data,pyaudio.paComplete)
    # open stream
    stream = p.open(format = p.get_format_from_width(f.getsampwidth()),
                                channels = f.getnchannels(),
                                rate = f.getframerate(),
                                output = True,
                                stream_callback=callback)
    # start data
    stream.start_stream()
    #Enter the while loop,when the Button is pressed
    while stream.is_active():
        global MusicKeyStatus
        MusicKeyStatus = keys.GetKeyStatus()
        time.sleep(0.01)  
    # stop stream
    stream.stop_stream()
    stream.close()
    # close PyAudio
    p.terminate()
def main():
    #Check the xxx.wav whether exist
    #Move to /tmp/scale/ if exist 
    if os.path.exists('/var/lib/cloud9/PocketBeagle/Grove/*.wav'): 
        GetCmdReturn('sudo mv /var/lib/cloud9/PocketBeagle/Grove/*.wav \
        /tmp/scale/')
    global files
    files= os.listdir("/tmp/scale")
    print(files)
    global MusciIndex
    MusciIndex = 0
    global keys
    keys = BUTTON()
    global Lcd
    Lcd = JHD1802()
    # Create timer thread that weak up after 0.25s 
    # The timer will execute the FunTimer after 0.25s     
    global timer
    timer = threading.Timer(0.25, FunTimer)
    timer.start() 
    while True:
        KeyStatus = keys.GetKeyStatus()
        #KeyStatus isn't empty when the Button is pressed
        if(len(KeyStatus)):
            #The KeyStatus[0] = 256 will play next music and the music name display on LCD
            if KeyStatus[0] == 256:
                MusciIndex = MusciIndex + 1
                if MusciIndex > 6:
                    MusciIndex = 0
            #The KeyStatus[0] = 257 will play last music and the music namedisplay on LCD 
            if KeyStatus[0] == 257:
                MusciIndex = MusciIndex - 1
                if MusciIndex < 0:
                    MusciIndex = 6
            PlayMusic("/tmp/scale/%s"%files[MusciIndex])
        time.sleep(0.05)
if __name__ == "__main__":
    main()