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

blink.py gets: ImportError: No module named Adafruit_BBIO.GPIO

blinky.rb, once installed give:
`require': cannot load such file -- beaglebone (LoadError)

The following files are:
analog2.js: ENOENT: no such file or directory, open '/sys/devices/platform/bone_capemgr/slots'
analog3.js
analog.js
blink.c
Blink.ino
blinkled.js
blink.py
blinky.rb
fade.js
input2.js
input.js
ledswipe.js
pwmTest.sh
shiftout.js
test.js