#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
import time
from ADC import ADC
from RGBLed import RGBLed
from LCD import LCD

def main():
    AIN = ADC()
    LED = RGBLed(2)
    Display = LCD()
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
        Display.set("Slider is %03d\nRotary is %03d" % (Slide_Potentiometer_Data, Rotary_Angle_Data))
        Rainbow_Index = Rotary_Angle_Data//40
        for i in range(len(Rainbow[Rainbow_Index])):
            Rainbow[Rainbow_Index][i] = Rainbow[Rainbow_Index][i] * Slide_Potentiometer_Data
        LED.set(0,Rainbow[Rainbow_Index][0],Rainbow[Rainbow_Index][1],Rainbow[Rainbow_Index][2])
        LED.set(1,Rainbow[Rainbow_Index][0],Rainbow[Rainbow_Index][1],Rainbow[Rainbow_Index][2])
        time.sleep(0.1)

if __name__ == "__main__":
    main()