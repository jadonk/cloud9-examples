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

var inputPin = "A5";

loop();

function loop() {
    var value = b.analogRead(inputPin);
    process.stdout.write(inputPin + ': ' + (value*100).toFixed(1) + '%, ' + (1.8*value).toFixed(3) + 'V   \r');
    setTimeout(loop, 100);
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
