#!/usr/bin/env node
////////////////////////////////////////
//	swipeLED.js
//      Blinks the USR LEDs in sequence.
//	Wiring:
//	Setup:	
//	See:	
////////////////////////////////////////
const fs = require('fs');
const leds = ['/sys/class/leds/beaglebone:green:usr0/brightness',
    '/sys/class/leds/beaglebone:green:usr1/brightness',
    '/sys/class/leds/beaglebone:green:usr2/brightness',
    '/sys/class/leds/beaglebone:green:usr3/brightness'];
var i = 0;
const delay = 100;

console.log('Hit ^C to stop');

console.log("Toggling LEDs:");
ledOn();

function ledOn() {
    process.stdout.write("\x1b[" + (n(i)+1) + "G1");
    fs.writeFileSync(leds[n(i)], 1);
    setTimeout(ledOff, delay);
}

function ledOff() {
    process.stdout.write("\x1b[" + (n(i)+1) + "G0");
    fs.writeFileSync(leds[n(i)], 0);
    i++; 
    if(i >= 2*leds.length-2) 
        i = 0;
    //i++; if(i > 3) i = 0;
    ledOn();
}

function n(i) {
    if(i >= leds.length) 
        return 2*leds.length-i-2;
    else 
        return i;
}
