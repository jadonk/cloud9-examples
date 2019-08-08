#!/usr/bin/env node
////////////////////////////////////////
//	analog2.js
//  Reads analog in on P9_36 synchronously and prints it.
//	Wiring:	Attach the outer pins on a variable resistor to P9_32 and P9_34.
//          Attach the wiper (middle pin) of the resistor to P9_36.
//	Setup:	
//	See:	
////////////////////////////////////////
var b = require('bonescript');

var inputPin = "P9_36";

loop();

function loop() {
    var value = b.analogRead(inputPin);
    console.log(value);
    setTimeout(loop, 100);
}
