# BMP085 I2C pressure/temperature sensor demo
The BMP085 is a readily available pressure/temperature sensor using I2C. 
It is directly supported by the Linux kernel, so all you have to do is ask 
the kernel to load the driver and then start reading values.

![alt text](tempPressure.png "I2C pressure/temperature sensor")

## Build and execute instructions

* Disconnect your board from power (including USB)
* Connect the pins as follows:

BMP085 | Pin       | Bone  | Pocket | Grove
-------| ---       | ----- | ------ | -----
GND    | GND       | P9_1  | P2_15
V+     | 3.3V      | P9_3  | P1_14
SCL    | I2C2 SCL  | P9_19 | P1_28  | I2C2-1
SDA    | I2C2 SDA  | P9_20 | P1_26  | I2C2-2

* Reapply power before running the demo code
