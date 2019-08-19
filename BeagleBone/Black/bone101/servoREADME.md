# Demo: Micro Servo Motor
*Output a pulse width modulated signal on a Servo Motor.*

The [Micro Servo Motor](http://www.adafruit.com/products/169) 
can rotate 180 degrees and is usually used in applications 
such as robotics, CNC machinery, or automated manufacturing. 
By using the```'analogWrite``` function [```analogWrite(pin, value, [freq], [callback])```, 
the BeagleBone will send Pulse Width Modulated Signals to control the Servo Motor. 
The position of the servo motor is set by the length of a pulse. 
In the following program, the frequency is set at 60Hz, which means that the 
servo receives a pulse every 16.66ms. The length of the pulse, or the duty cycle, 
can be changed from 3% to 14.5% and can be changed to rotate the servo motor.

The example below, when run, will adjust the position of the servo motor between its two extremes repeatitively.

More information regarding PWMs can be found on the 
[Wikipedia pulse-width modulation page](https://en.wikipedia.org/wiki/Pulse-width_modulation).

![alt text](servo.png "Micro Servo Motor")

## Build and execute instructions
* Connect the "GND" pin from the Servo Motor to P9_1 of the board
* Connect the "V+" pin from the Servo Motor to P9_3 of the board
* Connect a 1kohm resistor to the "PWM" pin of the Servo Motor and to P9_14 of the board.
* Click "Run" on the code. The value of 'position' will go between 0 and 1 
changing by 'increment' amount with updates every 200ms.
