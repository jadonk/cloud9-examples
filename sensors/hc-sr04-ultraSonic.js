#!/usr/bin/env node

// This is an example of reading HC-SR04 Ultrasonic Range Finder
// This version measures from the fall of the Trigger pulse 
//   to the end of the Echo pulse

const b = require('bonescript');
const util = require("util");

const trigger = 'P9_15',  // Pin to trigger the ultrasonic pulse
    echo    = 'P9_17',  // Pin to measure to pulse width related to the distance
    ms = 2500;           // Trigger period in ms
    
var startTime, pulseTime;
    
b.pinMode(echo,    b.INPUT);
b.pinMode(trigger, b.OUTPUT);

b.attachInterrupt(echo, pingEnd, b.FALLING);
 
b.digitalWrite(trigger, 1);     // Unit triggers on a falling edge.
                                // Set trigger to high so we call pull it low later

// Pull the trigger low at a regular interval.
setInterval(ping, ms);

// Pull trigger low and start timing.
function ping() {
    console.log('ping');
    b.digitalWrite(trigger, 0);
    startTime = process.hrtime();
}

// Compute the total time and get ready to trigger again.
function pingEnd(x) {
    // console.log("x: ", util.inspect(x));
    if(x.attached) {
        console.log("Interrupt handler attached: " + x.pin.key);
        return;
    }
    if(startTime) {
        pulseTime = process.hrtime(startTime);
        b.digitalWrite(trigger, 1);
        console.log('pulseTime = ' + (pulseTime[1]/1000000-0.8).toFixed(3));
    }
}
