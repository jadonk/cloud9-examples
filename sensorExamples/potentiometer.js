#!/usr/bin/env node
var b = require('bonescript');
b.analogRead('P9_40', printAIN1);

function printAIN1(err, value) {
    console.log('value = ' + value);
    console.log('err = ' + err);
}                    
