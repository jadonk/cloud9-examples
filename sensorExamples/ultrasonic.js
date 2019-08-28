#!/usr/bin/env node
var b = require('bonescript');
var analogVoltage;
const scale = 2;    // Set to 1 for Black and 2 for AI

// Ultrasound | Pin  | Bone  | Pocket
// ---------- | ---  | ----- | ------
// GND        | GND  | P9_1  | P2_15
// +5         | 3.3V | P9_3  | P1_14
// series with 3k ohm and 1.2k ohm resistor | A0 | P9_39 | P1_19

/* Check the sensor values every 2 seconds*/

console.log("scale set to", scale);
setInterval(read, 2000);

function read(){
    b.analogRead('A0', printStatus);
}

function printStatus(err, value) {
    var distanceInches;
    analogVoltage = value*1.8; // ADC Value converted to voltage
    console.log('value = ' + analogVoltage); 
    distanceInches = scale * analogVoltage / 0.00699;
    console.log("There is an object " + 
    parseFloat(distanceInches).toFixed(3) + " inches away.");
}

// Bone  | Pocket | AIN
// ----- | ------ | --- 
// P9_39 | P1_19  | A0
// P9_40 | P1_21  | A1
// P9_37 | P1_23  | A2
// P9_38 | P1_25  | A3
// P9_33 | P1_27  | A4
// P9_36 | P2_35  | A5
// P9_35 | P1_02  | A6
