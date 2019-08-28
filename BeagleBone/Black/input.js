#!/usr/bin/env node
////////////////////////////////////////
//	input.js
//      Responds to changes on P8_19 via a callback.
//	Wiring:	Connect P8_19 to P9_14 with a 1kOhm resistor.
//	Setup:	
//	See:	
////////////////////////////////////////
var b = require('bonescript');

var outputPin = "P9_14";
var inputPin  = "P8_19";
var ledPin    = "USR3";
var mydelay = 250;
var state   = b.LOW;

console.log('Please connect ' + inputPin + ' to ' + outputPin +
    ' with a 1kOhm resistor');
b.pinMode(inputPin, b.INPUT);
b.pinMode(outputPin, b.OUTPUT);
b.pinMode(ledPin, b.OUTPUT);

b.digitalWrite(outputPin, b.LOW);
b.attachInterrupt(inputPin, setLED, b.CHANGE);

toggle();

function setLED(x) {
    b.digitalWrite(ledPin, x.value);
}

function toggle() {
    state = (state == b.LOW) ? b.HIGH : b.LOW;
    b.digitalWrite(outputPin, state);
    setTimeout(toggle, mydelay);        // Waut a bit, and then toggle again
}
