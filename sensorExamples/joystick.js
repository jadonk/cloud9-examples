#!/usr/bin/env node
var b = require('bonescript');
var pos = {};

b.analogRead('P9_36', onX);

function onX(err, value) {
    pos.x= parseFloat(value * 100).toFixed(2);
    b.analogRead('P9_38', onY);
}

function onY(err, value) {
    pos.y = parseFloat(value * 100).toFixed(2);
	console.log(JSON.stringify(pos));
}
