# Demo: Reading a Distance Sensor (Variable Pulse Width Sensor)

You want to use a HC-SR04 Ultrasonic Range Sensor with BeagleBone Black.

The HC-SR04 Ultrasonic Range Sensor (shown in below) works by sending a trigger pulse to the _Trigger_ input and then measuring the pulse width on the _Echo_ output. The width of the pulse tells you the distance.

![alt text](hc-sr04.jpg "HC-SR04 Ultrasonic Sensor")

Wire the sensor as shown below. Note that the HC-SR04 is a 5 V
device, so the _banded_ wire (running from +P9_7+ on the Bone to VCC on the range finder) attaches the HC-SR04 to the Bone's 5 V power supply. 

![alt text](hc-sr04-ultraSonic_bb.png "Wiring an HC-SR04 Ultrasonic Sensor")

This code is more complex than others in this chapter, because we have to tell the device when to start measuring and time the return pulse.