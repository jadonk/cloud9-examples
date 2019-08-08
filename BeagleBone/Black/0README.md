This folder contains live demos that run on the BeagleBone Black.

Cookbook - contains support material for [BeagleBone Cookbook:
Software and Hardware Problems and Solutions](http://shop.oreilly.com/product/0636920033899.do) published by  O'Reilly Media.

pru - contains demos for the Programmable Real-time Unit

Notes:
I'm using P9_14 for the PRU, so we need to find another GPIO to use

    .js files run from command line, but gets the following from c9:
(node:19484) [DEP0062] DeprecationWarning: `node --debug` and `node --debug-brk` are invalid. Please use `node --inspect` or `node --inspect-brk` instead. 

blink.c compiles/runs from command line but get the following from c9:
Compiling /var/lib/cloud9/BeagleBone/Black/blink.c ...    

cc     blink.c   -o blink               
ERROR while launching the debugger:                 
        "gdbserver" is not installed 
gbdserver IS installed

The following files are:

analogInOut.js          // Reads analog in on P9_36 and adjusts the PWM on P9_14.
analogInSync.js         // Reads analog in on P9_36 synchronously and prints it.
analogInCallback.js     // Reads analog in on P9_36 and prints it via a callback.
blink.c         // Blinks the USR3 LED via c
blinkled.js     // Blinks the USR LEDs and P9_14
blink.py        // Blinks one LED wired to P9_14 via python
fade.js         // Fades the LED wired to P9_14 using the PWM.
input.js        // Responds to changes on P8_19 via a callback.
input2.js       // Responds to changes on P8_19 and P9_16 via callbacks.
ledswipe.js     // Blinks the USR LEDs in sequence.

Not Working or not able to test:
Blink.ino
blinky.rb       // -- beaglebone/spi (LoadError)
pwmTest.sh
shiftout.js     // Demonstrate shiftOut with a 7 segment display
