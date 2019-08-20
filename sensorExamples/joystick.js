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

b.analogRead('A5', onX);

function onX(err, value) {
    pos.x= parseFloat(value * 100).toFixed(2);
    b.analogRead('A3', onY);
}

function onY(err, value) {
    pos.y = parseFloat(value * 100).toFixed(2);
	console.log(JSON.stringify(pos));
}
