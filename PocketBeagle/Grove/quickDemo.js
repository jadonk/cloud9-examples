#!/usr/bin/env node
var b = require('bonescript');
var fs = require('fs');
var net = require('net');

var LCD = '/dev/lcd0';
var PROXIMITY = '/sys/bus/iio/devices/iio:device1/in_distance_raw';
var status = {
	lat: 0,
	lon: 0,
	alt: 0
};
var socket = new net.Socket();
socket.connect(2947);
socket.setEncoding('utf-8');
socket.on('data', onData);
socket.write('?WATCH={"enable":true,"json":true}');

if(!fs.existsSync(LCD)) {
	b.writeTextFile('/sys/bus/i2c/devices/i2c-1/new_device', 'hd44780 0x3e');
}
if(!fs.existsSync(PROXIMITY)) {
	// need to modprobe first
	b.writeTextFile('/sys/bus/i2c/devices/i2c-2/new_device', 'vl53l0x 0x29');
}

b.writeTextFile('/sys/class/hd44780/lcd0/cursor_display', 0);
b.writeTextFile('/sys/class/hd44780/lcd0/cursor_blink', 0);

function onData(data) {
	try {
		var dataArray = data.split('\n');
		for(var e in dataArray) {
			if(dataArray[e][0] == '{') {
				var newStatus = JSON.parse(dataArray[e]);
				if(newStatus.class == 'TPV') {
					for(var key in newStatus) {
						status[key] = newStatus[key];
					}
				}
			}
		}
	} catch(ex) {
		//console.log('Error in JSON object from gpsd: ' + ex + '\n' + data);
	}
	var prox = b.readTextFile(PROXIMITY).trim();
	var pos = 
		status.lat.toFixed(1) + ' ' +
		status.lon.toFixed(1) + ' ' +
		status.alt.toFixed(0);
	process.stdout.write('\r' + pos + ' ' + prox);
	b.writeTextFile(LCD, '\x1B[H\x1B[2J' + pos + '\n' + prox);
}

