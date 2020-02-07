#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# [Grove - 12 Key Capacitive I2C Touch Sensor V2]
# (http://wiki.seeedstudio.com/Grove-12_Key_Capacitive_I2C_Touch_Sensor_V2-MPR121/) on I2C2
# [Grove – Speaker](http://wiki.seeedstudio.com/Grove-Speaker/) 
# on UART2
# [Grove - Chainable RGB LED X 2](http://wiki.seeedstudio.com/Grove-Chainable_RGB_LED/) 
# on A2
import time
import wave
import pyaudio
from Captouch import MPR121
from RGBLed import P981X
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
    """Play WAV format music when the Mpr121 is pressed 
        file:the Wav format music
    """
    # define stream chunk 
    chunk = 1024
    # open a wav format music
    f = wave.open(file,"rb")
    # instantiate PyAudio
    p = pyaudio.PyAudio()
    #define callback function
    def callback(in_data, frame_count, time_info, status):
        data = f.readframes(frame_count)
        #the function will return pyaudio.paContinue when the Mpr121 is pressed 
        if Mpr121Data[0] != 0:
            return (data,pyaudio.paContinue)
        return (data,pyaudio.paComplete)
    # open stream
    stream = p.open(format = p.get_format_from_width(f.getsampwidth()),
                                channels = f.getnchannels(),
                                rate = f.getframerate(),
                                output = True,
                                stream_callback=callback)
    #Start stream 
    stream.start_stream()
    #Enter the while loop,when the Mpr121 is pressed
    while stream.is_active():
        global Mpr121Data
        Mpr121Data = Mpr121.get()
        time.sleep(0.01)  
    # stop stream
    stream.stop_stream()
    stream.close()
    f.close()
    # close PyAudio
    p.terminate()
def main():
    LED = P981X()
    global Mpr121
    Mpr121 = MPR121()
    while True:
        GetMpr121 = Mpr121.get()
        Mpr121Result = GetMpr121[1]
        #Mpr121Result isn't empty when the Mpr121 is pressed
        if any(Mpr121Result) != False:
        #Check the which one button is pressed on Mpr12 then play 
        #different music and turn on LED that will display different color
            for i in range(12):
                if(Mpr121Result[i] == 1):
                    if i > 3 :
                        LED.set(0,((i-4)&0x01)*255,((i-4)&0x02)*255,((i-4)&0x04)*255)
                        LED.set(1,((i-4)&0x01)*255,((i-4)&0x02)*255,((i-4)&0x04)*255)                    
                        Play_Music("/tmp/scale/%s"%_SCALE_DEFS[i-4])
                        
                    else :
                        LED.set(0,(i&0x01)*255,(i&0x02)*255,(i&0x04)*255)
                        LED.set(1,(i&0x01)*255,(i&0x02)*255,(i&0x04)*255)
                        if i == 0:
                            LED.set(0,50,50,200)
                            LED.set(1,50,50,200)
                        Play_Music("/tmp/scale/%s"%_SCALE_DEFS[i])
        else :
            LED.set(0,0,0,0)
            LED.set(1,0,0,0)
        time.sleep(0.05)
if __name__ == "__main__":
    main()