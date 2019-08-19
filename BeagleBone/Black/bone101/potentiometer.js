#!/usr/bin/env node
var b = require('bonescript');
b.analogRead('P9_40', printAIN1);

function printAIN1(x) {
    console.log('x.value = ' + x.value);
    console.log('x.err = ' + x.err);
}                    
