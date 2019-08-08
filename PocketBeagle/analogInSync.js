#!/usr/bin/env node
////////////////////////////////////////
//	analogInSync.js
//  Reads analog in on P1_19 synchronously and prints it.
//	Wiring:	Attach the outer pins on a variable resistor to P1_17 and P1_18.
//          Attach the wiper (middle pin) of the resistor to P1_19.
//	Setup:	
//	See:	
////////////////////////////////////////
var b = require('bonescript');

var inputPin = "P1_19";

loop();

function loop() {
    var value = b.analogRead(inputPin);
    process.stdout.write(inputPin + ': ' + (value*100).toFixed(1) + '%, ' + (1.8*value).toFixed(3) + 'V   \r');
    setTimeout(loop, 100);
}
