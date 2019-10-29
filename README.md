# Grove-Music-Kit-for-Pocket-Beagle


![](https://github.com/SeeedDocument/Grove-Music-Kit-for-Pocket-Beagle/raw/master/img/_DAS6325.jpg)




## Haedware Overview

![](https://github.com/SeeedDocument/Grove-Music-Kit-for-Pocket-Beagle/raw/master/img/pin.jpg)



**Part List:**

- <font size="4" color="red">①</font> [Grove - Sound Sensor](http://wiki.seeedstudio.com/Grove-Sound_Sensor/)
- <font size="4" color="red">②</font> [Grove - Chainable RGB LED](http://wiki.seeedstudio.com/Grove-Chainable_RGB_LED/)
- <font size="4" color="red">③</font> [Grove - Ultrasonic Distance Sensor](http://wiki.seeedstudio.com/Grove-Ultrasonic_Ranger/)
- <font size="4" color="red">④</font> [Grove - Rotary Angle Sensor](http://wiki.seeedstudio.com/Grove-Rotary_Angle_Sensor/)
- <font size="4" color="red">⑤</font> [Grove - Slide Potentiometer](http://wiki.seeedstudio.com/Grove-Slide_Potentiometer/)
- <font size="4" color="red">⑥</font> [Grove – Button](http://wiki.seeedstudio.com/Grove-Button/)
- <font size="4" color="red">⑦</font> [Grove - 12 Key Capacitive I2C Touch Sensor V2](http://wiki.seeedstudio.com/Grove-12_Key_Capacitive_I2C_Touch_Sensor_V2-MPR121/)
- <font size="4" color="red">⑧</font> [Grove - 3 Axis Digital Accelerometer](http://wiki.seeedstudio.com/Grove-3-Axis_Digital_Accelerometer-16g/)
- <font size="4" color="red">⑨</font> [Grove – Speaker](http://wiki.seeedstudio.com/Grove-Speaker/)
- <font size="4" color="red">⑩</font> [Grove – 16x2 LCD](http://wiki.seeedstudio.com/Grove-16x2_LCD_Series/)
- <font size="4" color="red">⑪</font> [Pocket Beaglebone with Grove shield](https://www.seeedstudio.com/PocketBeagle-OSD3358ARM-Cortex-A8-512MB-RAM-p-2888.html)
- <font size="4" color="red">⑫</font> [10pcs Alligator Cable](https://www.seeedstudio.com/10pcs-alligator-clip-test-lead-500mm-22awg-p-3087.html)
- <font size="4" color="red">⑬</font> SD+TF Card Reader
- <font size="4" color="red">⑭</font> WiFi Dongle
- <font size="4" color="red">⑮</font> Acrylic shell



---------------

## Lesson – 1. Control the Light

### Description:

In this lesson, students will light up the RGB LED, and learn how to use sound and potentiometer to change the color of RGB LED.

### Hardware Requirement:

- [Grove - Sound Sensor](http://wiki.seeedstudio.com/Grove-Sound_Sensor/)
- [Grove - Slide Potentiometer](http://wiki.seeedstudio.com/Grove-Slide_Potentiometer/)
- [Grove - Rotary Angle Sensor](http://wiki.seeedstudio.com/Grove-Rotary_Angle_Sensor/)
- [Grove - Chainable RGB LED](http://wiki.seeedstudio.com/Grove-Chainable_RGB_LED/)


### Hardware Connection
 
- Plug the Grove - Sound Sensor into **A5** port
- Plug the Grove - Slide Potentiometer into **A2** port
- Plug the Grove - Rotary Angle Sensor into **A0** port
- Grove - RGB LED in to **PWM** port
- Power the Pocket Beagle via the **micro USB** port


![](https://github.com/SeeedDocument/Grove-Music-Kit-for-Pocket-Beagle/raw/master/img/_DAS6312.jpg)


### Software

```
to be continue ... ...
```


-------------

## Lesson – 2. Musical Note

### Description:

In this lesson, students can move their hand in front of the ultrasonic sensor, the LCD will show the distance of the hand, and speaker will play different musical note based on different distance.

### Hardware Requirement:

- [Grove - Ultrasonic Distance Sensor](http://wiki.seeedstudio.com/Grove-Ultrasonic_Ranger/)
- [Grove – 16x2 LCD](http://wiki.seeedstudio.com/Grove-16x2_LCD_Series/)
- [Grove – Speaker](http://wiki.seeedstudio.com/Grove-Speaker/)


### Hardware Connection
 
- Plug the Grove - Ultrasonic Distance Sensor into **PWM** port
- Plug the Grove – 16x2 LCD into **I2C** port
- Plug the Grove – Speaker into **A5** port
- Power the Pocket Beagle via the **micro USB** port



![](https://github.com/SeeedDocument/Grove-Music-Kit-for-Pocket-Beagle/raw/master/img/project2.jpg)


### Software

```
to be continue ... ...
```

--------


## Lesson – 3. Switch the Music

### Description:

In this lesson, students will learn how to use the 2 buttons to select the next song or the last song. The LCD will show the name of the song.

### Hardware Requirement:

- [Grove – Button x 2](http://wiki.seeedstudio.com/Grove-Button/)
- [Grove – Speaker](http://wiki.seeedstudio.com/Grove-Speaker/)
- [Grove – 16x2 LCD](http://wiki.seeedstudio.com/Grove-16x2_LCD_Series/)


### Hardware Connection
 
- Plug the Grove – Button into **A2** and **A0** port
- Plug the Grove – 16x2 LCD into **I2C** port
- Plug the Grove – Speaker into **A5** port
- Power the Pocket Beagle via the **micro USB** port


![](https://github.com/SeeedDocument/Grove-Music-Kit-for-Pocket-Beagle/raw/master/img/project-3.jpg)


### Software

```
to be continue ... ...
```

-----

## Lesson – 4. Download Music via the WIFI dongle

### Description:
In this lesson, students will learn how to download mp3 files from the Internet via the WIFI dongle, and they can also practice the skill learn from Lesson3 to switch the music.

### Hardware Requirement:

- [Grove – Button x 2](http://wiki.seeedstudio.com/Grove-Button/)
- [Grove – Speaker](http://wiki.seeedstudio.com/Grove-Speaker/)
- [Grove – 16x2 LCD](http://wiki.seeedstudio.com/Grove-16x2_LCD_Series/)
- USB WIFI dongle


### Hardware Connection
 
- Plug the Grove – Button into **A2** and **A0** port
- Plug the Grove – 16x2 LCD into **I2C** port
- Plug the Grove – Speaker into **A5** port
- Plug the WiFi dongle into the **USB** Port
- Power the Pocket Beagle via the **micro USB** port


![](https://github.com/SeeedDocument/Grove-Music-Kit-for-Pocket-Beagle/raw/master/img/project-4.jpg)


### Software

```
to be continue ... ...
```


----


## Lesson – 5. KeyBoard Player

### Description:

In this lesson, students will learn how to use the capacitive touch sensor to play different musical note.

### Hardware Requirement:

- [Grove - 12 Key Capacitive I2C Touch Sensor V2](http://wiki.seeedstudio.com/Grove-12_Key_Capacitive_I2C_Touch_Sensor_V2-MPR121/)
- [Grove – Speaker](http://wiki.seeedstudio.com/Grove-Speaker/)


### Hardware Connection
 
- Plug the Grove – Speaker into **A5** port
- Plug the Grove - 12 Key Capacitive I2C Touch Sensor V2 into **I2C** port
- Power the Pocket Beagle via the **micro USB** port


![](https://github.com/SeeedDocument/Grove-Music-Kit-for-Pocket-Beagle/raw/master/img/project-5.jpg)


### Software

```
to be continue ... ...
```


----


## Lesson – 6. Start the Party


### Description:

In this lesson, students will learn how to use the capacitive touch sensor to play the song <Twinkle Star>. And the RGB LED will have different color based on different music note.

### Hardware Requirement:

- [Grove - 12 Key Capacitive I2C Touch Sensor V2](http://wiki.seeedstudio.com/Grove-12_Key_Capacitive_I2C_Touch_Sensor_V2-MPR121/)
- [Grove – Speaker](http://wiki.seeedstudio.com/Grove-Speaker/)
- [Grove - Slide Potentiometer](http://wiki.seeedstudio.com/Grove-Slide_Potentiometer/)
- [Grove - Chainable RGB LED](http://wiki.seeedstudio.com/Grove-Chainable_RGB_LED/)



### Hardware Connection
 
- Plug the Grove – Speaker into **A5** port
- Plug the Grove - 12 Key Capacitive I2C Touch Sensor V2 into **I2C** port
- Plug the Grove - Slide Potentiometer into **A2** port
- Plug the Chainable RGB LED into **PWM** port
- Power the Pocket Beagle via the **micro USB** port


![](https://github.com/SeeedDocument/Grove-Music-Kit-for-Pocket-Beagle/raw/master/img/project-6.jpg)


### Software

```
to be continue ... ...
```


----


## Lesson – 7. Music Box

### Description:

In this lesson, students will learn how to use the Grove – 3-Axis Accelerometer to control RGB LED and Speaker. At last, he can make a smart box, by putting different side of the box on the table, the box will have different color and play different music.


### Hardware Requirement:

- [Grove - 3 Axis Digital Accelerometer](http://wiki.seeedstudio.com/Grove-3-Axis_Digital_Accelerometer-16g/)
- [Grove – Speaker](http://wiki.seeedstudio.com/Grove-Speaker/)
- [Grove - Chainable RGB LED](http://wiki.seeedstudio.com/Grove-Chainable_RGB_LED/)


### Hardware Connection

- Plug the Grove – Speaker into **A5** port
- Plug the Grove - 3 Axis Digital Accelerometer into **A2** port
- Plug the Chainable RGB LED into **PWM** port
- Power the Pocket Beagle via the **micro USB** port

![](https://github.com/SeeedDocument/Grove-Music-Kit-for-Pocket-Beagle/raw/master/img/project-7.jpg)


### Software

```
to be continue ... ...
```


----