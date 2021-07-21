## Accelerometer

### Description:

In this lesson, students will learn how to use the Grove - 3-Axis Accelerometer to display the current x, y and z accelerations.

### Hardware Requirement:

- [Grove - 3 Axis Digital Accelerometer](http://wiki.seeedstudio.com/Grove-3-Axis_Digital_Accelerometer-16g/)

### Hardware Connection

- Plug the Grove - 3 Axis Digital Accelerometer into **I2C2** port
- Power PocketBeagle via the **micro USB** port

### Software

- Step 1. Enter Cloud9 by typing IP of PocketBeagle
- Step 2. Select PocketBeagle -> Grove
- Step 3. Run ./Accelerometer.py by using Runner:Python.

### Success
        Once the program starts, move the accelerometer around to see the values change.
```bash
bone$ ./Accelerometer.py 
[3, 1, 85]
[3, 0, 85]
[3, 0, 86]
[10, 0, 79]
[19, 0, 70]
[31, 0, 58]
```