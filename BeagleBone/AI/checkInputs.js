#!/usr/bin/env node
////////////////////////////////////////
//	checkinputs.js
//      Monitors all the predefined inputs. 
//	Wiring:	Toggle the input you want to test.
//	Setup:	
//	See:	
////////////////////////////////////////
const b = require('bonescript');

const inputs = ["P8_9", "P8_10", "P8_11", "P8_12", "P8_15", "P8_16", 
                "P8_33", "P8_35", "P8_38", 
                "P9_11", "P9_17", "P9_18", "P9_19", "P9_20", 
                "P9_22", "P9_25", "P9_27", "P9_29", "P9_42"];
var states = [];

for(var i in inputs) {
    b.pinMode(inputs[i], b.INPUT);
    states[i] = 0;
}

setInterval(check, 100);

function check() {
    var value;
    // console.log("check");
    for(var i in inputs) {
        value = b.digitalRead(inputs[i]);
        // console.log("value: ", value);
        if(states[i] !== value) {
            console.log(inputs[i], "changed to", value);
            states[i] = value;
        }
    }
}

// Not working: "P8_15", "P8_33", "P8_35", "P8_38", "P9_11", "P9_22", "P9_25", 