PocketBeagle tutorial and example code

These examples have been taken from many places and customized for PocketBeagle.

* Digi-Key shopping list: http://www.digikey.com/short/q8tmdv

![Breadboard Wiring Diagram](PocketBeagle-examples1_bb.png "PocketBeagle Breadboard Wiring")

The following files are:

File                | Description
----                | -----------
analogInOut.js      | Reads analog in and adjusts the PWM.
analogInSync.js     | Reads analog in synchronously and prints it.
analogInCallback.js | Reads analog in and prints it via a callback.
blinkLED.c          | Blinks the USR3 LED via c
blinkLED.js         | Blinks the USR LEDs and P9_14
blinkLED.py         | Blinks one LED via python
fadeLED.js          | Fades the LED using the PWM.
input.js            | Responds to changes on input via a callback.
input2.js           | Responds to changes on 2 inputs via callbacks.
swipeLED.js         | Blinks the USR LEDs in sequence.
