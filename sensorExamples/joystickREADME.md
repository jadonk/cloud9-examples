# Demo: Adafruit 2-Axis Thumb Joystick

The [Analog 2-axis Thumb Joystick](http://www.adafruit.com/products/512) 
allows you to easily mount a PSP/Xbox-like thumb joystick to your project. 
Using analog pins, the BeagleBone will read and determine both the X and Y axis. 
The joystick also includes an extra digital input that will let you read the switch.

*The console will output both the x-axis and y-axis with readings from 0-100, 
with (50,50) being the center location.*

![alt text](joystick.png "Joystick")

## Build and execute instructions
* Connect the following pins

Joysitck | Pin     | Bone  | Pocket
-------- | ---     | ----- | ------
VCC      | 1.8V    | P9_32 | P1_18
GND      | GND     | P9_34 | P1_17
HOR      | A5      | P9_36 | P2_35
VER      | A3      | P9_38 | P1_25
SEL      | GPIO0_7 | P9_42 | P2_29

* Click "Run" and it will output both the x and y axis, with 50,50 being the center.
