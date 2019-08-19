#!/usr/bin/env node
var b = require('bonescript');
var pos = {};

b.analogRead('P9_36', onX);

function onX(x) {
    pos.x = parseFloat(x.value * 100).toFixed(2);
    b.analogRead('P9_38', onY);
}

function onY(x) {
    pos.y = parseFloat(x.value * 100).toFixed(2);
	console.log(JSON.stringify(pos));
}
