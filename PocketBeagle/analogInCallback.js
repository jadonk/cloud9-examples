#!/usr/bin/env node
////////////////////////////////////////
//	analog2.js
//  Reads analog in on P1_19 and prints it via a callback.
//	Wiring:	Attach the outer pins on a variable resistor to P1_17 and P1_18.
//          Attach the wiper (middle pin) of the resistor to P1_19.
//	Setup:	
//	See:	
////////////////////////////////////////
var b = require('bonescript');
var pin = 'P1_19';

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
