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

var inputPin = "A0";

loop();

function loop() {
    var value = b.analogRead(inputPin);
    process.stdout.write(inputPin + ': ' + (value*100).toFixed(1) + '%, ' + (1.8*value).toFixed(3) + 'V   \r');
    setTimeout(loop, 100);
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
