#!/usr/bin/env node
// This uses the eQEP hardware to read a rotary encoder

const fs = require('fs');

// Black
// eQEP0:	P9.27 and P9.42
// eQEP1:	P9.33 and P9.35
// eQEP2:	P8.11 and P8.12
const eQEP0 = "/sys/devices/platform/ocp/48300000.epwmss/48300180.eqep/",
	  eQEP1 = "/sys/devices/platform/ocp/48302000.epwmss/48302180.eqep/",
	  eQEP2 = "/sys/devices/platform/ocp/48304000.epwmss/48304180.eqep/"

// AI\
// eQEP1:	P8.33 and P8.35
// eQEP2:	P8.11 and P8.12 or P9.19 and P9.41
// eQEP3:	P8.24 abd P8.25 or P9.27 and P9.42
const eQEP1AI = "/sys/devices/platform/44000000.ocp/4843e000.epwmss/4843e180.eqep/",
      eQEP2AI = "/sys/devices/platform/44000000.ocp/48440000.epwmss/48440180.eqep/",
      eQEP3AI = "/sys/devices/platform/44000000.ocp/48442000.epwmss/48442180.eqep/"
    
const eQEP = eQEP1AI;
	
var oldData,			// pervious data read
    period = 100;		// in ms

// Set pinmux for P8_11 and P8_12 on Black
// fs.writeFile("/sys/devices/platform/ocp/ocp:P8_11_pinmux/state", "qep", function(err) {
// 	if (err) console.log("writeFile err: ", err);
// });
// fs.writeFile("/sys/devices/platform/ocp/ocp:P8_12_pinmux/state", "qep", function(err) {
// 	if (err) console.log("writeFile err: ", err);
// });

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