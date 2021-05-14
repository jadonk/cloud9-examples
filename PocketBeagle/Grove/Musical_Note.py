#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# [Grove - Ultrasonic Distance Sensor](http://wiki.seeedstudio.com/Grove-Ultrasonic_Ranger/)
# on A0
# [Grove - 16x2 LCD](http://wiki.seeedstudio.com/Grove-16x2_LCD_Series/) on I2C1
# [Grove - Speaker Plus](http://wiki.seeedstudio.com/Grove-Speaker/) on UART2
import wave
import pyaudio
from tqdm import tqdm
import time
from UltrasonicSensor import HCSR04
from LCD import JHD1802
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
    """Play WAV format music
        file:the Wav format music
    """
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
    # play stream
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
def main():
    Distance = HCSR04()
    Lcd = JHD1802()
    while True:
        distance = Distance.GetDistance()
        #Display the distance
        Lcd.SetText("The Distance: \r\n{} cm".format(distance))
        print("Distance is %3d \r" %distance, end = '')
        #Speaker will play different music when the HCSR04 gets a different distance
        if distance < 240:
            Play_Music("/tmp/scale/%s"%_SCALE_DEFS[distance//40])
        time.sleep(1)
if __name__ == "__main__":
    main()