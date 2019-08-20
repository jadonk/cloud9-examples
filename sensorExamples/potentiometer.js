#!/usr/bin/env node
var b = require('bonescript');

// Potentiometer  | Pin  | Bone  | Pocket
// -------------- | ---  | ----- | ------
// outer terminal | 1.8V | P9_32 | P1_18
// outer terminal | GND  | P9_34 | P1_17
// wiper (middle) | A1   | P9_40 | P1_21

b.analogRead('A1', printAIN1);

function printAIN1(err, value) {
    console.log('value = ' + value);
    if(err) {
        console.log('err = ' + err);
    }
}                    
