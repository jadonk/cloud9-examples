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
# [Grove - Slide Potentiometer](https://www.seeedstudio.com/Grove-Slide-Potentiometer.html) on A0
# [Grove - Rotary Angle Sensor](http://wiki.seeedstudio.com/Grove-Rotary_Angle_Sensor/) on A5
# [Grove - Chainable RGB LED](http://wiki.seeedstudio.com/Grove-Chainable_RGB_LED/) on A2
# [Grove - 16x2 LCD](http://wiki.seeedstudio.com/Grove-16x2_LCD_Series/) on I2C1
import time
from ADC import ADC
from RGBLed import P981X
from LCD import JHD1802

def main():
    AIN = ADC()
    LED = P981X()
    Display = JHD1802()
    while True:
        Rainbow = [[1,0,0],[1,0.5,0],[1,1,0],[0,1,0],[0,1,1],[0,0,1],[1,0,1]]
        SlidePotentiometerData = AIN.get(0)
        RotaryAngleData = AIN.get(5)
        #Scale down the value of ADC to 0~255
        SlidePotentiometerData = int(SlidePotentiometerData)*255//3800
        RotaryAngleData = int(RotaryAngleData)*255//3800
        
        if RotaryAngleData > 240:
            RotaryAngleData = 240
        if SlidePotentiometerData > 255 :
            SlidePotentiometerData = 255
            
        print("SlidePotentiometerData is %3d   RotaryAngleData is %3d  \r" %
            (SlidePotentiometerData, RotaryAngleData), end = '')
        #Display the Slide Potentiometer Data and Rotary Angle Data on LCD
        Display.SetText("Slider is %03d\nRotary is %03d" % (SlidePotentiometerData, RotaryAngleData))
        #Get the Rainbow Index by Rotary Angle
        RainbowIndex = RotaryAngleData//40
        #Set the brightness of LED by Slide Potentiometer
        for i in range(len(Rainbow[RainbowIndex])):
            Rainbow[RainbowIndex][i] = Rainbow[RainbowIndex][i] * SlidePotentiometerData
        #Light up the LED
        LED.set(0,Rainbow[RainbowIndex][0],Rainbow[RainbowIndex][1],Rainbow[RainbowIndex][2])
        LED.set(1,Rainbow[RainbowIndex][0],Rainbow[RainbowIndex][1],Rainbow[RainbowIndex][2])
        
        time.sleep(0.1)

if __name__ == "__main__":
    main()