This folder contains live demos that run on the BeagleBone Black.

Cookbook - contains support material for [BeagleBone Cookbook:
Software and Hardware Problems and Solutions](http:|shop.oreilly.com/product/0636920033899.do) published by  O'Reilly Media.

pru - contains demos for the Programmable Real-time Unit

The following files are:

File                | Description
----                | -----------
analogInOut.js      | Reads analog in on P9_36 and adjusts the PWM on P9_14.
analogInSync.js     | Reads analog in on P9_36 synchronously and prints it.
analogInCallback.js | Reads analog in on P9_36 and prints it via a callback.
blinkLED.c          | Blinks the USR3 LED via c
blinkLED.js         | Blinks the USR LEDs and P9_14
blinkLED.py         | Blinks one LED wired to P9_14 via python
fadeLED.js          | Fades the LED wired to P9_14 using the PWM.
input.js            | Responds to changes on P8_19 via a callback.
input2.js           | Responds to changes on P8_19 and P9_16 via callbacks.
swipeLED.js         | Blinks the USR LEDs in sequence.
