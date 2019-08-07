#!/usr/bin/env node
////////////////////////////////////////
//	analog.js
//  Reads analog in on P9_36 and adjusts the PWM on P9_14.
//	Wiring:	Attach the outer pins on a variable resistor to P9_32 and P9_34.
//          Attach the wiper (middle pin) of the resistor to P9_36.
//          P9_14 connects to the plus lead of an LED.  The negative lead of the
//			LED goes to a 220 Ohm resistor.  The other lead of the resistor goes
//			to ground.
//	Setup:	
//	See:	
////////////////////////////////////////
var b = require('bonescript');

var inputPin  = "P9_36";
var outputPin = "P9_14";

b.pinMode(outputPin, b.ANALOG_OUTPUT);
loop();

function loop() {
    var value = b.analogRead(inputPin);
    // console.log("loop: value = " + value);
    b.analogWrite(outputPin, value);
    setTimeout(loop, 10);
}
