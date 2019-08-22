#!/usr/bin/env node
// Run before: sudo chgrp i2c /sys/class/i2c-adapter/i2c-2/new_device
//             sudo chmod g+w /sys/class/i2c-adapter/i2c-2/new_device
const b = require('bonescript');
const fs = require('fs');
const bus = 2;
const model = 'bmp280';
const iic = '/sys/class/i2c-adapter/i2c-' + bus + '/';

//Sensor Locations on the BeagleBone Black
var temperature = '/sys/bus/i2c/drivers/' + model + '/' + bus + '-0077/iio:device1/in_temp_input';
var pressure    = '/sys/bus/i2c/drivers/' + model + '/' + bus + '-0077/iio:device1/in_pressure_input';

// We will initialize the driver for the BMP085 sensor located at I2C location 0x77
// This will cause an error it if is already there
b.writeTextFile(iic + 'new_device', 'bmp085 0x77');

// Opens,reads, and prints pressure and temperature
b.readTextFile(pressure, printPressure);
b.readTextFile(temperature, printTemperature); 

// Prints Pressure
function printPressure(err, x) {
   x = x.slice(0,-1);   // Remove trailing \n
   x *= 10;
   console.log("Pressure: ", x + " millibar");
   console.log("or:       ", x/33.86 + " inHg");
}

// Prints Temperature
function printTemperature(err, x) {
   x = x.slice(0,-1);   // Remove trailing \n
   x /= 1000;           // conver to degrees
   // '\xB0' is the degree symbol in hexademical
   console.log("Temperature: ", x + '\xB0' + " Celcius");
   console.log("or:          ", 1.8*x+32 + '\xB0' + " Fahrenheit"); 
}
