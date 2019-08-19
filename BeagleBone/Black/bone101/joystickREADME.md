# Demo: Adafruit 2-Axis Thumb Joystick

The [Analog 2-axis Thumb Joystick](http://www.adafruit.com/products/512) 
allows you to easily mount a PSP/Xbox-like thumb joystick to your project. 
Using analog pins, the BeagleBone will read and determine both the X and Y axis. 
The joystick also includes an extra digital input that will let you read the switch.

*The console will output both the x-axis and y-axis with readings from 0-100, 
with (50,50) being the center location.*

![alt text](joystick.png "Joystick")

## Build and execute instructions
* Connect the "VCC" pin from the joystick to P9_32 of the BeagleBone.
* Connect the "VER" pin from the joystick to P9_38 of the BeagleBone.
* Connect the "HOR" pin from the joystick to P9_36 of the BeagleBone.
* Connect the "SEL" pin from the joystick to P9_42 of the BeagleBone.
* Connect the "GND" pin from the joystick to P9_34 of the BeagleBone.
* Click "Run" and it will output both the x and y axis, with 50,50 being the center.