#!/usr/bin/env node
var b = require('bonescript');
var net = require('net')
var socket = new net.Socket();
var status = {
	lat: 0,
	lon: 0,
	alt: 0
};
socket.connect(2947);
socket.setEncoding('utf-8');
socket.on('data', onData);
socket.write('?WATCH={"enable":true,"json":true}');

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
	var pos = 
		status.lat.toFixed(1) + ' ' +
		status.lon.toFixed(1) + ' ' +
		status.alt.toFixed(0);
	process.stdout.write('\r' + pos);
	b.writeTextFile('/dev/lcd0', '\x1B[2J\x1B[H' + pos);
}

