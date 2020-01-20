# Description:

In this lesson, students will learn how to install the snowboy of Kitt-AI and use it.

## Hardware Requirement:

- [Grove - Analog Microphone](http://wiki.seeedstudio.com/Grove-Speaker/)
- [Grove - Chainable RGB LED X 2](http://wiki.seeedstudio.com/Grove-Chainable_RGB_LED/)

## Hardware Connection

- Plug the Grove - Speaker Plus into **UART2** port
- Plug the Grove - Analog Microphone into **PWM** port
- Power the Pocket Beagle via the micro **USB** port are 


## Software

- Step 1. Enter Cloud9 by typing IP of Pocket Beagle
- Step 2. Select PocketBeagle -> Grove -> Lesson-8.Hello-Kitt-AI
- Step 3. Search Ok_Beagle hotword model through [snowboy](https://snowboy.kitt.ai/dashboard)
- Step 4. Click the `Record and Download` to provide data of sound for Ok_Beagle.
- Step 5. Download the Ok_Beagle.pmdl from the [website](https://snowboy.kitt.ai/hotword/46889)
- Step 6. Move Ok_Beagle.pmdl to ~/snowboy/resources/models/
![](../img/Ok_Beagle.png)
- Step 7. Run the Ok_Beagel.py by using Runner:Python.

## success
        Pocket will light up when we say Ok_Beagle to mic.
