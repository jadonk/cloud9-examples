#!/usr/bin/env node
// Run before: 
//    sudo chgrp i2c /sys/class/i2c-adapter/i2c-2/new_device
//    sudo chmod g+w /sys/class/i2c-adapter/i2c-2/new_device
const b = require('bonescript');
const bus = 2;    // 2 for Black, 3 for AI
const addr = '40';
const model = 'si7020';
const i2c = '/sys/class/i2c-adapter/i2c-' + bus + '/';
const device = 'iio:device1';

//Sensor Locations on the BeagleBone
var temperature = i2c+bus+'-00'+addr+'/'+device+'/in_temp_scale';
var humidity    = i2c+bus+'-00'+addr+'/'+device+'/in_humidityrelative_scale';

// We will initialize the driver for the si7020 sensor located at I2C location 0x40
// This will cause an error it if is already there
b.writeTextFile(i2c + 'new_device', model+' 0x'+addr);

// Opens,reads, and prints humidity and temperature
b.readTextFile(humidity, printHumidity);
b.readTextFile(temperature, printTemperature); 

// Prints Humidity
function printHumidity(err, x) {
   if(err) console.log("printHumidity err: ", err);
   x = x.slice(0,-1);   // Remove trailing \n
   console.log("Humidity: ", x );
}

// Prints Temperature
function printTemperature(err, x) {
   if(err) console.log("printTemperture err: ", err);
   x = x.slice(0,-1);   // Remove trailing \n
   // '\xB0' is the degree symbol in hexademical
   console.log("Temperature: ", x + '\xB0' + " Celcius");
   console.log("or:          ", 1.8*x+32 + '\xB0' + " Fahrenheit"); 
}
