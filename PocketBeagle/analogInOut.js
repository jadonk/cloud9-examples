#!/usr/bin/env node
////////////////////////////////////////
//	analogInOut.js
//  Reads analog in on P1_19 and adjusts the PWM on P1_36.
//	Wiring:	Attach the outer pins on a variable resistor to P1_17 and P1_18
//          Attach the wiper (middle pin) of the resistor to P1_19.
//          P91_36 connects to the plus lead of an LED.  The negative lead of the
//			LED goes to a 220 Ohm resistor.  The other lead of the resistor goes
//			to 3.3V (P1_14).
//	Setup:	
//	See:	
////////////////////////////////////////
const b = require('bonescript');

const inputPin  = "A0";
const outputPin = "P1_36";

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
// P9_39 | P1_19  | 0
// P9_40 | P1_21  | 1
// P9_37 | P1_23  | 2
// P9_38 | P1_25  | 3
// P9_33 | P1_27  | 4
// P9_36 | P2_35  | 5
// P9_35 | P1_02  | 6
