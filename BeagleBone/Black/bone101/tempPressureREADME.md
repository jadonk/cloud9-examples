# BMP085 I2C pressure/temperature sensor demo
The BMP085 is a readily available pressure/temperature sensor using I2C. 
It is directly supported by the Linux kernel, so all you have to do is ask 
the kernel to load the driver and then start reading values.

![alt text](tempPressure.png "I2C pressure/temperature sensor")

## Build and execute instructions

* Disconnect your board from power (including USB)
* Connect BMP085 GND to P9_1
* Connect BMP085 VCC to P9_3
* Connect BMP085 SCL to P9_19
* Connect BMP085 SDA to P9_20
* Reapply power and refresh this page before running the demo code
