#!/usr/bin/env node
var b = require('bonescript');
var LED = "P9_15";
var AL  = "P9_29";

b.pinMode(LED, b.OUTPUT);
b.pinMode(AL, b.INPUT);

setInterval(checkPIR, 2500); // Checks the Sensor Every 2.5 Seconds

function checkPIR(){
    b.digitalRead(AL, printStatus);
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
