#!/usr/bin/env node
var b = require('bonescript');
var led = "P8_13";
b.pinMode(led, 'out');
b.pinMode('P8_19', b.INPUT);
setInterval(checkPIR, 2500); // Checks the Sensor Every 2.5 Seconds

function checkPIR(){
b.digitalRead('P8_19', printStatus);
}

function printStatus(err, value) {
    if(value === 0){
         b.digitalWrite(led, 1);
    console.log("Motion Detected");
    }
    else{
    console.log("No Motion Detected");
         b.digitalWrite(led, 0);
    }
}
