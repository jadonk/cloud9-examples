#!/usr/bin/env node
var fs = require('fs');
var os = require('os');
var process = require('process');
var child_process = require('child_process');

var buffer = Buffer.alloc(64);

child_process.execSync("make -f /var/lib/cloud9/common/Makefile TARGET=pruspeak.pru0");
fs.open("/dev/rpmsg_pru30", "r+", null, onOpen);

function onOpen(err, fd) {
    if (err) {
        console.log("Unble to open /dev/rpmsg_pru30");
        os.exit(-1);
    }
    fs.read(fd, buffer, 0, 60, null, onData);
    
    process.stdin.setEncoding('utf8');
    process.stdin.on('readable', onStdin);
    console.log("Type botspeak command and press <ENTER>");
    
    function onStdin(err) {
        var chunk;
        if (err) {
            console.log("Error reading from /dev/rpmsg_pru30");
            os.exit(-1);
        }
        while ((chunk = process.stdin.read()) !== null) {
            fs.write(fd, chunk);
        }
    }

    function onData(err, bytes, data) {
        if(err) {
            console.log("Error reading from /dev/rpmsg_pru30");
            os.exit(-1);
        }
        console.log('response: ' + data.toString('ascii'));
        fs.read(fd, buffer, 0, 60, null, onData);
    }
}

