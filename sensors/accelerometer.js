#!/usr/bin/env node
const b = require('bonescript');
const zeroOffset  = 0.4584;
const conversionFactor = 0.0917;

// Accelerometer | Pin  | Bone  | Pocket
// ------------- | ---  | ----- | ------
// GND           | GND  | P9_1  | P2_15
// VCC           | 3.3V | P9_3  | P1_14
// X             | A5   | P9_36 | P2_35
// Y             | A3   | P9_38 | P1_25
// Z             | A1   | P9_40 | P1_21

function callADC(){
    b.analogRead('A5', printX);
    b.analogRead('A3', printY);
    b.analogRead('A1', printZ);
}

function printX(err, value) {
    value = (value - zeroOffset)/conversionFactor;
    console.log('Analog Read Value x: ' +value);    
    // when the ADXL335 resting flat on a table or
    //board, then readings should be x:0
}

function printY(err, value) {
    value = (value - zeroOffset)/conversionFactor;
    console.log('Analog Read Value y: ' +value);
    // when the ADXL335 resting flat on a table or
    //board, then readings should be y:0
}

function printZ(err, value) {
    value = (value - zeroOffset)/conversionFactor;
    console.log('Analog Read Value z: ' +value);    
    // when the ADXL335 resting flat on a table or 
    //board, then readings should be z:1
    console.log('');
}

//callADC will be invoked 20 times a sec or once every 50 ms
var loop = setInterval(callADC, 50);          

function clear(){
    clearInterval(loop);
}

//after 1 second (1000ms), the interval
setTimeout(clear, 1000);                                
