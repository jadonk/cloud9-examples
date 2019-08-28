#!/usr/bin/env node
var b = require('bonescript');

// Potentiometer  | Pin  | Bone  | Pocket
// -------------- | ---  | ----- | ------
// outer terminal | 1.8V | P9_32 | P1_18
// outer terminal | GND  | P9_34 | P1_17
// wiper (middle) | A5   | P9_46 | P1_21

function start() {
    b.analogRead('A2', printA);
}

setInterval(start, 500);

function printA(err, value) {
    console.log('value = ' + value);
    if(err) {
        console.log('err = ' + err);
    }
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
