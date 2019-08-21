#!/usr/bin/env node
var b = require('bonescript');
var LED = "P9_14";
var AL  = "P8_19";

b.pinMode(LED, b.OUTPUT);
b.pinMode(AL, b.INPUT);

setInterval(checkPIR, 2500); // Checks the Sensor Every 2.5 Seconds

function checkPIR(){
    b.digitalRead('P8_19', printStatus);
}

function printStatus(err, value) {
    if(value === 0) {
        b.digitalWrite(LED, 1);
        console.log("Motion Detected");
    }
    else{
        console.log("No Motion Detected");
        b.digitalWrite(LED, 0);
    }
}
