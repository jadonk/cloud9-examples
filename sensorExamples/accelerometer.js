#!/usr/bin/env node
var b = require('bonescript');
var zeroOffset  = 0.4584;
var conversionFactor = 0.0917;

function callADC(){
    b.analogRead('P9_36', printX);
    b.analogRead('P9_38', printY);
    b.analogRead('P9_40', printZ);
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
