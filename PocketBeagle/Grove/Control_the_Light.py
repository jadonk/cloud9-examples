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
        Slide_Potentiometer_Data = AIN.get(0)
        Rotary_Angle_Data = AIN.get(5)
        Slide_Potentiometer_Data = int(int(Slide_Potentiometer_Data)/3800*255)
        Rotary_Angle_Data = int(int(Rotary_Angle_Data)/3800*255)
        if Rotary_Angle_Data > 240:
            Rotary_Angle_Data = 240
        if Slide_Potentiometer_Data > 255 :
            Slide_Potentiometer_Data = 255
        print("Slide_Potentiometer_Data is %3d   Rotary_Angle_Data is %3d  \r" %
            (Slide_Potentiometer_Data, Rotary_Angle_Data), end = '')
        Display.SetText("Slider is %03d\nRotary is %03d" % (Slide_Potentiometer_Data, Rotary_Angle_Data))
        Rainbow_Index = Rotary_Angle_Data//40
        for i in range(len(Rainbow[Rainbow_Index])):
            Rainbow[Rainbow_Index][i] = Rainbow[Rainbow_Index][i] * Slide_Potentiometer_Data
        LED.set(0,Rainbow[Rainbow_Index][0],Rainbow[Rainbow_Index][1],Rainbow[Rainbow_Index][2])
        LED.set(1,Rainbow[Rainbow_Index][0],Rainbow[Rainbow_Index][1],Rainbow[Rainbow_Index][2])
        time.sleep(0.1)

if __name__ == "__main__":
    main()