#!/usr/bin/env node
var b = require('bonescript');
var analogVoltage = 0;

// Ultrasound | Pin  | Bone  | Pocket
// ---------- | ---  | ----- | ------
// GND        | GND  | P9_1  | P2_15
// +5         | 3.3V | P9_3  | P1_14
// series with 3k ohm and 1.2k ohm resistor | A1 | P9_40 | P1_21

/* Check the sensor values every 2 seconds*/
setInterval(read, 2000);

function read(){
    b.analogRead('A1', printStatus);
}

function printStatus(err, value) {
    var distanceInches;
    analogVoltage = value*1.8; // ADC Value converted to voltage
    console.log('value = ' + analogVoltage); 
    distanceInches = analogVoltage / 0.00699;
    console.log("There is an object " + 
    parseFloat(distanceInches).toFixed(3) + " inches away.");
}
