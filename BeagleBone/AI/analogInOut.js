#!/usr/bin/env node
////////////////////////////////////////
//	analogInOut.js
//  Reads analog in on P9_36 and adjusts the PWM on P9_14.
//	Wiring:	Attach the outer pins on a variable resistor to P9_32 and P9_34.
//          Attach the wiper (middle pin) of the resistor to P9_36.
//          P9_14 connects to the plus lead of an LED.  The negative lead of the
//			LED goes to a 220 Ohm resistor.  The other lead of the resistor goes
//			to ground.
//	Setup:	
//	See:	
////////////////////////////////////////
const b = require('bonescript');

const inputPin  = "A3";
const outputPin = "P9_14";

console.log('Hit ^C to stop');
b.pinMode(outputPin, b.ANALOG_OUTPUT);
setTimeout(loop, 200);  // work-around to wait for PWM permissions

function loop() {
    var value = b.analogRead(inputPin);
    process.stdout.write(inputPin + '-->' + outputPin + ': ' + (value*100).toFixed(1) + '%   \r');
    b.analogWrite(outputPin, value);
    setTimeout(loop, 10);
}

// Bone  | Pocket | AIN
// ----- | ------ | --- 
// P9_39 | P1_19  | A0
// P9_40 | P1_21  | A1
// P9_37 | P1_23  | A2
// P9_38 | P1_25  | A3
// P9_33 | P1_27  | A4
// P9_36 | P2_35  | A5
// P9_35 | P1_02  | A6
