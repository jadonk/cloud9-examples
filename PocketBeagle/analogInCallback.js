#!/usr/bin/env node
////////////////////////////////////////
//	analogInCallback.js
//  Reads analog in on P1_19 and prints it via a callback.
//	Wiring:	Attach the outer pins on a variable resistor to P1_17 and P1_18.
//          Attach the wiper (middle pin) of the resistor to P1_19.
//	Setup:	
//	See:	
////////////////////////////////////////
const b = require('bonescript');
const pin = 'A0';

console.log('Hit ^C to stop');
b.analogRead(pin, printStatus);

function printStatus(err, x) {
    if(err) {
        console.log('Got error: ' + err); 
        return;
    };
    process.stdout.write(pin + ': ' + (x*100).toFixed(1) + '%, ' + (1.8*x).toFixed(3) + 'V   \r');
    b.analogRead(pin, printStatus);
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
