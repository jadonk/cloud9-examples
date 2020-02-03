# Description:

In this lesson, students can move their hand in front of the ultrasonic distance sensor, the LCD will show the distance of the hand, and speaker will play different musical note based on different distance.

## Hardware Requirement:

- [Grove - Ultrasonic Distance Sensor](http://wiki.seeedstudio.com/Grove-Ultrasonic_Ranger/)
- [Grove - 16x2 LCD](http://wiki.seeedstudio.com/Grove-16x2_LCD_Series/)
- [Grove - Speaker Plus](http://wiki.seeedstudio.com/Grove-Speaker/)


## Hardware Connection
 
- Plug the Grove - Ultrasonic Distance Sensor into **A0** port
- Plug the Grove - 16x2 LCD into **I2C1** port
- Plug the Grove - Speaker Plus into **UART2** port
- Power PocketBeagle via the **micro USB** port

![](../img/project2.jpg)

## Software

- Step 1. Enter Cloud9 by typing IP of Pocket Beagle
- Step 2. Select PocketBeagle -> Grove -> Lesson-2.Musical-Note
- Step 3. Run the tone_generator.py by using Runner:Python.
- Step 4. Run the Musical_Note.py by using Runner:Python.

## Success
        Now please please slowly change the distance between your hand and the ultrasonic distance sensor, you can find the distance value in the LCD change and the music switched by the distance.