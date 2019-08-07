#!/usr/bin/env node
////////////////////////////////////////
//	analog2.js
//  Reads analog in on P9_36 and prints it via a callback.
//	Wiring:	Attach the outer pins on a variable resistor to P9_32 and P9_34.
//          Attach the wiper (middle pin) of the resistor to P9_36.
//	Setup:	
//	See:	
////////////////////////////////////////
var b = require('bonescript');

var inputPin = "P9_36";

loop();

function loop() {
    b.analogRead(inputPin, function(err, resp){
        console.log(resp);
        setTimeout(loop, 100);
    });

}
