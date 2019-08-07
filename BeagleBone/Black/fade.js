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
var b = require('bonescript');

// setup starting conditions
var awValue = 0.01;
var awDirection = 1;
var awPin = "P9_14";

// configure pin 
b.pinMode(awPin, b.ANALOG_OUTPUT);

// call function to update brightness every 10ms
setInterval(fade, 10);

// function to update brightness
function fade() {
    b.analogWrite(awPin, awValue);
    awValue = awValue + (awDirection*0.01);
    if(awValue > 1.0) { 
        awValue = 1.0; awDirection = -1; 
        }
    else if(awValue <= 0.01) { 
        awValue = 0.01; awDirection = 1; 
        }
}
