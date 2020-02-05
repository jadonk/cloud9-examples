# Copyright (c) 2020 SeeedStudio
# Author: Hansen Chen
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# [Grove - Ultrasonic Distance Sensor](http://wiki.seeedstudio.com/Grove-Ultrasonic_Ranger/) on A0
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
        #Speaker will play different music When the HCSR04 get different distance
        if distance < 240:
            Play_Music("/tmp/scale/%s"%_SCALE_DEFS[distance//40])
        time.sleep(1)

if __name__ == "__main__":
    main()