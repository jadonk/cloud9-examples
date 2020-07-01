#!/usr/bin/env node
//////////////////////////////////////
// 	pushbutton.js
// 	Reads the Left pushbutton.
//////////////////////////////////////
// Pre-steps (may need to eventually put in this program):
//   * Make sure /sys/class/gpio/gpio45 is exported
//   * Make sure pinmux is in gpio mode
//   * Make sure gpio is in input mode
var Epoll = require('epoll').Epoll;
var fs = require('fs');
var button = fs.openSync("/sys/class/gpio/gpio45/value", "r");  // P2_33
var buffer = Buffer.alloc(1);

fs.writeFileSync('/sys/class/gpio/gpio45/edge', "both");
doRead(button);
var poller = new Epoll(printStatus);
poller.add(button, Epoll.EPOLLPRI);
console.log("Ready. Please press 'L' button on TechLab. Hit ^C to stop.");

function doRead(fd) {
  fs.readSync(fd, buffer, 0, 1, 0);
  process.stdout.write('value = ' + buffer.toString() + '          \r');
}

function printStatus(err, fd, events) {
  if(err) {
    console.log('err = ' + err);
    return;
  }
  doRead(fd);
}
