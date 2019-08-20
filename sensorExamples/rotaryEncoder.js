#!/usr/bin/env node
// This uses the eQEP hardware to read a rotary encoder

var fs = require('fs');
    
var eQEP0 = "/sys/devices/platform/ocp/48300000.epwmss/48300180.eqep/",
    eQEP1 = "/sys/devices/platform/ocp/48302000.epwmss/48302180.eqep/",
    eQEP2 = "/sys/devices/platform/ocp/48304000.epwmss/48304180.eqep/",
    eQEP = eQEP2;
	
var oldData,			// pervious data read
    period = 100;	// in ms

// Set pinmux for P8_11 and P8_12
fs.writeFile("/sys/devices/platform/ocp/ocp:P8_11_pinmux/state", "qep", function(err) {
	if (err) throw err;
});
fs.writeFile("/sys/devices/platform/ocp/ocp:P8_12_pinmux/state", "qep", function(err) {
	if (err) throw err;
});

// Set the eEQP period, convert to ns.
fs.writeFile(eQEP+'period', period*1000000, function(err) {
	if (err) throw err;
	console.log('Period updated to ' + period*1000000);
});

// Enable
fs.writeFile(eQEP+'enabled', 1, function(err) {
	if (err) throw err;
	console.log('Enabled');
});

setInterval(readEncoder, period);    // Check state every 250 ms

function readEncoder(x) {
	fs.readFile(eQEP + 'position', {encoding: 'utf8'}, printValue);
}

function printValue(err, data) {
	if (err) throw err;
	if (oldData !== data) {
		console.log('position: '+data+' speed: '+(oldData-data));
		oldData = data;
	}
}