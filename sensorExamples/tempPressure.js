#!/usr/bin/env node
// Run before: sudo chgrp i2c /sys/class/i2c-adapter/i2c-2/new_device
//             sudo chmod g+w /sys/class/i2c-adapter/i2c-2/new_device
const b = require('bonescript');
const fs = require('fs');
const bus = 3;    // 2 for Black, 3 for AI
const addr = '77';
const model = 'bmp280';
const i2c = '/sys/class/i2c-adapter/i2c-' + bus + '/';
const device = 'iio:device1';

//Sensor Locations on the BeagleBone
var temperature = i2c+bus+'-00'+addr+'/'+device+'/in_temp_input';
var pressure    = i2c+bus+'-00'+addr+'/'+device+'/in_pressure_input';

// We will initialize the driver for the BMP085 sensor located at I2C location 0x77
// This will cause an error it if is already there
b.writeTextFile(i2c + 'new_device', model+' 0x'+addr);

// Opens,reads, and prints pressure and temperature
b.readTextFile(pressure, printPressure);
b.readTextFile(temperature, printTemperature); 

// Prints Pressure
function printPressure(err, x) {
   if(err) console.log("printPressure err: ", err);
   x = x.slice(0,-1);   // Remove trailing \n
   x *= 10;
   console.log("Pressure: ", x + " millibar");
   console.log("or:       ", x/33.86 + " inHg");
}

// Prints Temperature
function printTemperature(err, x) {
   if(err) console.log("printTemperture err: ", err);
   x = x.slice(0,-1);   // Remove trailing \n
   x /= 1000;           // conver to degrees
   // '\xB0' is the degree symbol in hexademical
   console.log("Temperature: ", x + '\xB0' + " Celcius");
   console.log("or:          ", 1.8*x+32 + '\xB0' + " Fahrenheit"); 
}
