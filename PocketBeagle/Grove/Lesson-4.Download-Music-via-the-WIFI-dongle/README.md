# Description:

In this lesson, students will learn how to use the 2 buttons to select the next song or the last song. the buttons not only can select the next song or the last song by press instantly but also can play music by Press longly.

The LCD will show the name of the song.

## Hardware Requirement:

- [Grove - Button x 2](http://wiki.seeedstudio.com/Grove-Button/)
- [Grove - Speaker Plus](http://wiki.seeedstudio.com/Grove-Speaker/)
- [Grove - 16x2 LCD](http://wiki.seeedstudio.com/Grove-16x2_LCD_Series/)

## Hardware Connection
 
- Plug the Grove - Button into **A5** and **UART4** port
- Plug the Grove - 16x2 LCD into **I2C1** port
- Plug the Grove - Speaker Plus into **UART2** port
- Plug the WiFi dongle into the **USB** Port
- Power PocketBeagle via the **micro USB** port


![](../img/project-4.jpg)


## Software

- Step 1.Connect wifi that connects with your computer by using `connmanctl`

if you don't know how to use `connmanctl`, maybe you should review the previous lessons

- Step 2.Download [winscp](https://winscp.net/eng/download.php).

- Step 3. Open winscp and type the hostname and username 

![](../img/winscp.png)
the hostname is an IP address of Pockbeagle that can use ifconfig to find it. The username is `debian`

- Step 4. Drag your music file to `/home/debian/scale`(Please select xxx.wav to /home/debian/scale)

![](../img/drag_music_file.png)

- Step 5. Enter Cloud9 by typing IP of Pocket Beagle
- Step 6. Select PocketBeagle -> Grove -> Lesson-4.Download-Music-via-the-WIFI-dongle
- Step 7. Run the Musical_Note.py by using Runner:Python.

## success

        Default music is boring and bad taste? Now, with the help of WiFi, you can download the music meet your own flavor.