#!/usr/bin/env node
var b = require('bonescript');
var XINPUT = '/sys/bus/iio/devices/iio:device1/in_accel_x_raw';
var YINPUT = '/sys/bus/iio/devices/iio:device1/in_accel_y_raw';
var ZINPUT = '/sys/bus/iio/devices/iio:device1/in_accel_z_raw';

console.log('Hit ^C to stop');
doAccelRead();

function doAccelRead() {
  writeNum('x', b.readTextFile(XINPUT));
  writeNum('y', b.readTextFile(YINPUT));
  writeNum('z', b.readTextFile(ZINPUT));
  process.stdout.write('\r');
  setTimeout(doAccelRead, 100);
}

function writeNum(axis, value) {
  value = "" + value.trim();
  while(value.length < 4) {
    value = " " + value;
  }
  process.stdout.write(axis + ': ' + value + '   ');
}