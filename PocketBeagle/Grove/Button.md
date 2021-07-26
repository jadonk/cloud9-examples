## Button

### Description:

In this lesson, students will learn how to display the status of the 2 buttons.

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
Pressing the right button (**BTN_**) displays:

```bash
bone$ ./Button.py 
event at 1627313516.074140, code 256, type 01, val 01
[256]
key event at 1627313516.074140, 256 (['BTN_0', 'BTN_MISC']), down
event at 1627313516.074140, code 00, type 00, val 00
event at 1627313516.654546, code 256, type 01, val 00
[]
key event at 1627313516.654546, 256 (['BTN_0', 'BTN_MISC']), up
event at 1627313516.654546, code 00, type 00, val 00
```
The left button (**BTN_1**) shows:
```bash
event at 1627313517.871746, code 257, type 01, val 01
[257]
key event at 1627313517.871746, 257 (BTN_1), down
event at 1627313517.871746, code 00, type 00, val 00
event at 1627313518.376610, code 257, type 01, val 00
[]
key event at 1627313518.376610, 257 (BTN_1), up
event at 1627313518.376610, code 00, type 00, val 00
```
