# Description:

In this lesson, students will learn how to use the capacitive touch sensor to play the song <Twinkle Star>. And the RGB LED will have different color based on different music note.

### Hardware Requirement:

- [Grove - Speaker Plus](http://wiki.seeedstudio.com/Grove-Speaker/)
- [Grove - Analog Microphone](http://wiki.seeedstudio.com/Grove-Chainable_RGB_LED/)


## Hardware Connection

- Plug the Grove - Speaker Plus into **UART2** port
- Plug the Grove - Analog Microphone into **PWM** port
- Power the Pocket Beagle via the **micro USB** port

![](../img/project-7.jpg)

## Software

- Step 1.Connect wifi that connects with your computer by using `connmanctl`

if you don't know how to use `connmanctl`, maybe you should review the previous lessons

- Step 2.Download [winscp](https://winscp.net/eng/download.php).

- Step 3. Open winscp and type the hostname and username 

![](../img/winscp.png)
the hostname is an IP address of Pockbeagle that can use ifconfig to find it. The username is `debian`

- Step 4. Drag your music file to `/home/debian/scale`(Please select *.wav to /home/debian/scale)

![](../img/drag_music_file.png)

- Step 5. Enter Cloud9 by typing IP of Pocket Beagle
- Step 6. Select PocketBeagle -> Grove -> Lesson-4.Download-Music-via-the-WIFI-dongle
- Step 7. Run the Musical_Note.py by using Runner:Python.

## success
        Just control the music as lesson 5, and you can see the color of RGB LED change.