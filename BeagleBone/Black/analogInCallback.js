#!/usr/bin/env node
////////////////////////////////////////
//	analogInCallback.js
//  Reads analog in on P9_36 and prints it via a callback.
//	Wiring:	Attach the outer pins on a variable resistor to P9_32 and P9_34.
//          Attach the wiper (middle pin) of the resistor to P9_36.
//	Setup:	
//	See:
////////////////////////////////////////
const b = require('bonescript');

const inputPin = "A5";

console.log('Hit ^C to stop');
b.analogRead(inputPin, printStatus);

function printStatus(err, x) {
    if(err) {
        console.log('Got error: ' + err); 
        return;
    };
    process.stdout.write(inputPin + ': ' + (x*100).toFixed(1) + '%, ' + (1.8*x).toFixed(3) + 'V   \r');
    b.analogRead(inputPin, printStatus);
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
