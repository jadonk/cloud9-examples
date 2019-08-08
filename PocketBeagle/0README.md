PocketBeagle tutorial and example code

These examples have been taken from many places and customized for PocketBeagle.

* Digi-Key shopping list: http://www.digikey.com/short/q8tmdv

![Breadboard Wiring Diagram](PocketBeagle-examples1_bb.png "PocketBeagle Breadboard Wiring")

The following files are:

analogInOut.js      // Reads analog in on P1_19 and adjusts the PWM on P1_36.
analogInSync.js     // Reads analog in on P1_19 synchronously and prints it.
analogInCallback.js // Reads analog in on P1_19 and prints it via a callback.
blinkLED.c          // Blinks the USR3 LED via c
blinkLED.js         // Blinks the USR LEDs and P1_36
blinkLED.py         // Blinks one LED wired to P1_36 via python
fadeLED.js          // Fades the LED wired to P1_36 using the PWM.
input.js            // Responds to changes on P8_19 via a callback.
input2.js           // Responds to changes on P8_19 and P9_16 via callbacks.
swipeLED.js         // Blinks the USR LEDs in sequence.
