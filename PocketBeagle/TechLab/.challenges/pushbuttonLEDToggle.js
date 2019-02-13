#!/usr/bin/env node
var b = require('bonescript');
var l_button = "P2_33";
var r_button = "P1_29";

console.log('Hit ^C to stop');
console.log("Please press 'L'(on) or 'R'(off) button on TechLab.");
b.pinMode(l_button, b.INPUT, 7, null, null, doAttachL);
b.pinMode(r_button, b.INPUT, 7, null, null, doAttachR);

function doAttachL(err, x) {
  if(err) {
    console.log('pinMode err = ' + err);
    return;
  }
  b.attachInterrupt(l_button, true, b.FALLING, turnOn);
}

function doAttachR(err, x) {
  if(err) {
    console.log('pinMode err = ' + err);
    return;
  }
  b.attachInterrupt(r_button, true, b.FALLING, turnOff);
}

function turnOn(err, x) {
  if(err) {
    console.log('attachInterrupt err = ' + err);
    return;
  }
  if(x.attached) {
    return;
  }
  process.stdout.write('value = on          \r');
  
  b.digitalWrite("USR3", 1);
}

function turnOff(err, x) {
  if(err) {
    console.log('attachInterrupt err = ' + err);
    return;
  }
  if(x.attached) {
    return;
  }
  process.stdout.write('value = off          \r');
  
  b.digitalWrite("USR3", 0);
}
