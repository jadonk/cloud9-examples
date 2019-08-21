#!/usr/bin/env node
////////////////////////////////////////
//	analogInCallback.js
//  Reads analog in on P9_36 and prints it via a callback.
//	Wiring:	Attach the outer pins on a variable resistor to P9_32 and P9_34.
//          Attach the wiper (middle pin) of the resistor to P9_36.
//	Setup:	
//	See:
////////////////////////////////////////
var b = require('bonescript');

var inputPin = "A5";

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
// P9_39 | P1_19  | 0
// P9_40 | P1_21  | 1
// P9_37 | P1_23  | 2
// P9_38 | P1_25  | 3
// P9_33 | P1_27  | 4
// P9_36 | P2_35  | 5
// P9_35 | P1_02  | 6
