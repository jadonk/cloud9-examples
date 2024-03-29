#!/usr/bin/env node
var b = require('bonescript');
var pos = {};

// Joysitck | Pin     | Bone  | Pocket
// -------- | ---     | ----- | ------
// VCC      | 1.8V    | P9_32 | P1_18
// GND      | GND     | P9_34 | P1_17
// HOR      | A5      | P9_36 | P2_35
// VER      | A3      | P9_38 | P1_25
// SEL      | GPIO0_7 | P9_42 | P2_29

var HOR = 'A6';     // A4
var VER = 'A2';     // A3
var SEL = 'P9_18';
b.pinMode(SEL, b.INPUT, 7, 'pullup');

function start() {
    b.analogRead(HOR, onX);
}

setInterval(start, 500);
b.attachInterrupt(SEL, readButton, b.CHANGE);

function readButton(x) {
    console.log("readButton: ", x.pin.key, x.value);
}

function onX(err, value) {
    pos.x= parseFloat(value * 100).toFixed(2);
    b.analogRead(VER, onY);
}

function onY(err, value) {
    pos.y = parseFloat(value * 100).toFixed(2);
	console.log(JSON.stringify(pos), b.digitalRead(SEL));
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
