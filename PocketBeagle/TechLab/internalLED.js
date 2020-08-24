#!/usr/bin/env node
//////////////////////////////////////
// 	internaLED.js
// 	Blinks the internal USR3 LED.
//////////////////////////////////////
var fs = require('fs');
var LED = '/sys/class/leds/beaglebone:green:usr3/brightness';
var state = 0;     // Initial state

setInterval(flash, 250); // Change state every 250 ms

function flash() {
  fs.writeFileSync(LED, state);
  if(state == 1) {
    state = 0;
  } else {
    state = 1;
  }
}
