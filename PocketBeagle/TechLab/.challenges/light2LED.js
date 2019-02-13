#!/usr/bin/env node
var b = require('bonescript');
var INPUT = 'P1_19';
var OUTPUT = '/sys/class/leds/techlab::blue/brightness';

console.log('Hit ^C to stop');
updateStatus();

function updateStatus() {
  var brightness = parseInt(b.analogRead('P1_19')*255);
  b.writeTextFile(OUTPUT, brightness);
  setTimeout(updateStatus, 20);
}