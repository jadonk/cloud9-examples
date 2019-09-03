#!/usr/bin/env node

// attachInterrupt err = attachInterrupt: requires Epoll module


////////////////////////////////////////
//	pushbutton.js
//      Responds to changes on P8_19 and P9_16 via callbacks.
//	Wiring:	Connect P8_19 to P9_14 with a 1kOhm resistor
//          Connect P9_15 to P9_16 with a 1kOhm resistor
//	Setup:	npm install epoll
//	See:	
////////////////////////////////////////
const b = require('bonescript');
const button = "P2_3";

console.log('Hit ^C to stop');
b.pinMode(button, b.INPUT, 7, 'pulldown', 'fast', doAttach);

function doAttach(err, x) {
    if(err) {
        console.log('pinMode err = ' + err);
        return;
    }
    b.attachInterrupt(button, true, b.CHANGE, printStatus);
}

function printStatus(err, x) {
    if(err) {
        console.log('attachInterrupt err = ' + err);
        return;
    }
    if(x.attached) {
        console.log("Interrupt handler attached");
        return;
    }
    process.stdout.write('value = ' + x.value + ', err   = ' + err + '          \r');
}
