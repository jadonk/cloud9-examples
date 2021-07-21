## Lesson - 2. Musical Note

### Description:

In this lesson, students can move their hands in front of the ultrasonic distance sensor, the LCD will show the distance of the hand, and the speaker will play different musical notes based on different distances.

### Hardware Requirement:

- [Grove - Ultrasonic Distance Sensor](http://wiki.seeedstudio.com/Grove-Ultrasonic_Ranger/)
- [Grove - 16x2 LCD](http://wiki.seeedstudio.com/Grove-16x2_LCD_Series/)
- [Grove - Speaker Plus](http://wiki.seeedstudio.com/Grove-Speaker/)


### Hardware Connection
 
- Plug the Grove - Ultrasonic Distance Sensor into **A0** port
- Plug the Grove - 16x2 LCD into **I2C1** port
- Plug the Grove - Speaker Plus into **UART2** port
- Plug the WiFi dongle into the **USB** Port
- Power PocketBeagle via the **micro USB** port

![](img/project2.jpg)

### Software

- Step 1. Enter Cloud9 IDE by typing IP of PocketBeagle
- Step 2. Select PocketBeagle -> Grove
- Step 3. Run the ToneGenerator.py by using Runner:Python.

**NOTE** : we should run ToneGenerator.py when we restart after.

- Step 4. Run the Musical_Note.py by using Runner:Python.

### Success
        Now please slowly change the distance between your hand and the ultrasonic distance sensor, you can find the distance value in the LCD change and the music switched by the distance.

