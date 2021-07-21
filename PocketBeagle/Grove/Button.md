## Button

### Description:

In this lesson, students will learn how to displaly the status of the 2 buttons.

### Hardware Requirement:

- [Grove – Button x 2](http://wiki.seeedstudio.com/Grove-Button/)

### Hardware Connection
 
- Plug the Grove – Button into **A5** and **UART4** port
- Plug the WiFi dongle into the **USB** Port
- Power PocketBeagle via the **micro USB** port

### Software

- Step 1. Enter Cloud9 IDE by typing IP of PocketBeagle
- Step 2. Select PocketBeagle -> Grove
- Step 3. Run the Button.py by using Runner:Python.

### Success
        Press the two buttons and you will see details about the button being pressed.

```bash
bone$ ./Button.py 
event at 1626882012.420934, code 257, type 01, val 01
[257]
key event at 1626882012.420934, 257 (BTN_1), down
event at 1626882012.420934, code 00, type 00, val 00
event at 1626882012.709587, code 257, type 01, val 00
[]
key event at 1626882012.709587, 257 (BTN_1), up
event at 1626882012.709587, code 00, type 00, val 00
event at 1626882013.886262, code 257, type 01, val 01
```
