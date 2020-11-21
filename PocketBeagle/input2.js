#!/usr/bin/env node
////////////////////////////////////////
//	input2.js
//      Responds to changes on P1_33 and P1_34 via callbacks.
//	Wiring:	Connect P1_33 to P1_36 with a 1kOhm resistor
//          Connect P1_34 to P1_35 with a 1kOhm resistor
//	Setup:	
//	See:	
////////////////////////////////////////
const b = require('bonescript');

const outputPin = "P1_36";
const inputPin  = "P1_33";
const outputPin2 = "P1_35";
const inputPin2  = "P1_34";
const ledPin  = "USR3";
const ledPin2 = "USR2";
const mydelay = 100;
const mydelay2 = 33;
var toggleState = b.LOW;
var toggleState2 = b.LOW;

console.log('Please connect ' + inputPin + ' to ' + outputPin +
    ' with a 1kOhm resistor');
console.log('Please connect ' + inputPin2 + ' to ' + outputPin2 +
    ' with a 1kOhm resistor');
b.pinMode(inputPin, b.INPUT);
b.pinMode(outputPin, b.OUTPUT);
b.pinMode(ledPin, b.OUTPUT);
b.pinMode(inputPin2, b.INPUT);
b.pinMode(outputPin2, b.OUTPUT);
b.pinMode(ledPin2, b.OUTPUT);

b.digitalWrite(outputPin, b.LOW);
b.digitalWrite(outputPin2, b.LOW);
b.attachInterrupt(inputPin, inputHandler, b.CHANGE);
b.attachInterrupt(inputPin2, inputHandler2, b.CHANGE);

toggle();
toggle2();

function inputHandler(x) {
    b.digitalWrite(ledPin, x.value);
}

function inputHandler2(x) {
    b.digitalWrite(ledPin2, x.value);
}

function toggle() {
    toggleState = (toggleState == b.LOW) ? b.HIGH : b.LOW;
    b.digitalWrite(outputPin, toggleState);
    setTimeout(toggle, mydelay);
}

function toggle2() {
    toggleState2 = (toggleState2 == b.LOW) ? b.HIGH : b.LOW;
    b.digitalWrite(outputPin2, toggleState2);
    setTimeout(toggle2, mydelay2);
}
