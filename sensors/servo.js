#!/usr/bin/env node
const b = require('bonescript');
const SERVO = 'P9_14';
const duty_min = 0.03;
var position = 0;
var increment = 0.1;
var timer;

b.pinMode(SERVO, b.OUTPUT);
updateDuty();

function updateDuty() {
    // compute and adjust duty_cycle based on
    // desired position in range 0..1
    var duty_cycle = (position*0.115) + duty_min;
    b.analogWrite(SERVO, duty_cycle, 60, scheduleNextUpdate);
    console.log("Duty Cycle: " + 
        parseFloat(duty_cycle*100).toFixed(1) + " %");   
}

function scheduleNextUpdate() {
    // adjust position by increment and 
    // reverse if it exceeds range of 0..1
    position = position + increment;
    if(position < 0) {
        position = 0;
        increment = -increment;
    } else if(position > 1) {
        position = 1;
        increment = -increment;
    }
    
    // call updateDuty after 200ms
    timer = setTimeout(updateDuty, 200);
}

// Turn motor off when done
process.on('SIGINT', function() {
    console.log('Got SIGINT, turning motor off');
    clearTimeout(timer);            // Stop the timer
    b.analogWrite(SERVO, 0, 60);    // Turn motor off
});
