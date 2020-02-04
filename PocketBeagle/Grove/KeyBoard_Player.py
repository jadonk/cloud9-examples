#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# [Grove - 12 Key Capacitive I2C Touch Sensor V2](http://wiki.seeedstudio.com/Grove-12_Key_Capacitive_I2C_Touch_Sensor_V2-MPR121/) on I2C2
# [Grove – Speaker](http://wiki.seeedstudio.com/Grove-Speaker/) on UART2
import time
import wave
import pyaudio
from Captouch import MPR121
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
Mpr121Data = [0]*2
def Play_Music(file):
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
        global Mpr121
        global Mpr121Data
        Mpr121Data = Mpr121.get()
        time.sleep(0.01)  

    # stop stream
    stream.stop_stream()
    stream.close()
    f.close()
    # close PyAudio
    p.terminate()
    
Mpr121 = MPR121()
def main():
    while True:
        GetMpr121 = Mpr121.get()
        # print(GetMpr121)
        Mpr121Result = GetMpr121[1]
        if any(Mpr121Result) != False:
            for i in range(12):
                if(Mpr121Result[i] == 1):
                    if i > 3 :
                        Play_Music("/tmp/scale/%s"%_SCALE_DEFS[i-4])
                    else :
                        Play_Music("/tmp/scale/%s"%_SCALE_DEFS[i])
        time.sleep(0.05)
if __name__ == "__main__":
    main()