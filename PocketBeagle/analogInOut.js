#!/usr/bin/env node
////////////////////////////////////////
//	analogInOut.js
//  Reads analog in on P91_19 and adjusts the PWM on P1_36.
//	Wiring:	Attach the outer pins on a variable resistor to P1_17 and P1_18
//          Attach the wiper (middle pin) of the resistor to P1_19.
//          P91_36 connects to the plus lead of an LED.  The negative lead of the
//			LED goes to a 220 Ohm resistor.  The other lead of the resistor goes
//			to 3.3V (P1_14).
//	Setup:	
//	See:	
////////////////////////////////////////
var b = require('bonescript');

var inputPin  = "P1_19";
var outputPin = "P1_36";

console.log('Hit ^C to stop');
b.pinMode(outputPin, b.ANALOG_OUTPUT);
setTimeout(loop, 200);  // work-around to wait for PWM permissions

function loop() {
    var value = b.analogRead(inputPin);
    process.stdout.write(inputPin + '-->' + outputPin + ': ' + (value*100).toFixed(1) + '%   \r');
    b.analogWrite(outputPin, value);
    setTimeout(loop, 10);
}
