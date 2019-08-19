#!/usr/bin/env node
var b = require('bonescript');
var i2c = '/sys/class/i2c-adapter/i2c-1/';
b.writeTextFile(i2c + 'new_device', 'bmp085 0x77');
var graphDataSize = 50;
window.graphData = new Array(graphDataSize);
var canvas = document.getElementById("canvas1");
var processing = new Processing(canvas, sketchProc);
for(var i=0; i < graphDataSize; i++) {
    window.graphData[i] = 0.5;
}
updateGraph(0.5);

function readTemp() {
    b.readTextFile(i2c + '1-0077/temp0_input', onRead);   
}

function onRead(x) {
    updateGraph(parseInt(x.data, 10)/200.0-0.9);
}

function updateGraph(x) {
    for(var i=0; i < graphDataSize; i++) {
        if(i == graphDataSize - 1) window.graphData[i] = x;
        else window.graphData[i] = window.graphData[i+1];
    }
    processing.redraw();
    setTimeout(readTemp, 300);
}

function sketchProc(p) {
    p.size(500, 300);

    // local variables
    var stepX = p.width / (graphDataSize - 1);

    p.noLoop();
    p.draw = function() {
        // erase background
        p.background(224);

        // draw axis
        p.stroke(25);
        p.strokeWeight(1);
        p.line(0, p.height/2, p.width, p.height/2);

        // draw graph
        p.stroke(2);
        p.strokeWeight(3);
        var lastX = 0, nextX = 0, lastY, nextY;
        for(var i=0; i < graphDataSize; i++) {
            nextY = p.height-window.graphData[i]*p.height;
            if(i != 0) {
                p.line(lastX, lastY, nextX, nextY);
                lastX += stepX;
            }
            nextX += stepX;
            lastY = nextY;
        }
    };
}
