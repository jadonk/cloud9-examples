#!/usr/bin/env node
////////////////////////////////////////
//	fade.js
//      Fades the LED wired to P9_14 using the PWM.
//	Wiring:	P9_14 connects to the plus lead of an LED.  The negative lead of the
//			LED goes to a 220 Ohm resistor.  The other lead of the resistor goes
//			to ground.
//	Setup:	
//	See:	
////////////////////////////////////////
const b = require('bonescript');
const LED = 'P9_14';  // Pin to use
var   step = 0.02;    // Step size
const min = 0.02,     // dimmest value
      max = 1;        // brightest value
var brightness = min; // Current brightness;

b.pinMode(LED, b.ANALOG_OUTPUT);
setTimeout(doInterval, 200);  // work-around to wait for PWM permissions

console.log('Hit ^C to stop');

function doInterval(err, x) {
    if(err) {
        console.log('err = ' + err);
        return;
    }
    setInterval(fade, 20);      // Step every 20 ms
}

function fade() {
    b.analogWrite(LED, brightness);
    brightness += step;
    if(brightness >= max || brightness <= min) {
        step = -1 * step;
    }
}
