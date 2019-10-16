#!/usr/bin/env node
////////////////////////////////////////
//	blinkLED.js
//      Blinks the USR LEDs and P9_14.
//	Wiring:	P9_14 connects to the plus lead of an LED.  The negative lead of the
//			LED goes to a 220 Ohm resistor.  The other lead of the resistor goes
//			to ground.
//	Setup:	
//	See:	
////////////////////////////////////////
const b = require('bonescript');

const leds = ["USR0", "USR1", "USR2", "USR3", "P9_14"];

for(var i in leds) {
    b.pinMode(leds[i], b.OUTPUT);
}

var state = b.HIGH;
for(var i in leds) {
    b.digitalWrite(leds[i], state);
}

setInterval(toggle, 250);

function toggle() {
    if(state == b.LOW) 
        state = b.HIGH;
    else
        state = b.LOW;
    for(var i in leds) {
        b.digitalWrite(leds[i], state);
    }
}
