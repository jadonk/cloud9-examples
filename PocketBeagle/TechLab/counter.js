#!/usr/bin/env node
var b = require('bonescript');

var L_BUTTON = "P2_33";
var R_BUTTON = "P1_29";
var debounceActive = false;
var counter = 0;

writeDigit(0, getDigit(0));
writeDigit(1, getDigit(0));

b.pinMode(L_BUTTON, b.INPUT, 7, null, null);
b.attachInterrupt(L_BUTTON, true, b.FALLING, onPress);
b.pinMode(R_BUTTON, b.INPUT, 7, null, null);
b.attachInterrupt(R_BUTTON, true, b.FALLING, onPress);
console.log('Hit ^C to exit');

function onPress(err, x) {
    var button = "";
    if(err) {
        return;
    }
    if(x && x.pin && x.pin.key) {
        switch(x.pin.key) {
            case L_BUTTON:
                button = "L";
                break;
            case R_BUTTON:
                button = "R";
                break;
            default:
                break;
        }
    }
    if(x.attached) {
        console.log("Interrupt handler for " + button + " attached");
        return;
    }
    if(debounceActive) {
        return;
    }
    debounceActive = true;
    //console.log(button + " pressed");
    if(button == "L") {
        counter--;
        if(counter < 0) counter = 0;
        writeCount(counter);
    }
    if(button == "R") {
        counter++;
        if(counter > 0xff) counter = 0xff;
        writeCount(counter);
    }
    setTimeout(clearDebounce, 150);
    return true;
}

function clearDebounce() {
    debounceActive = false;
}

function writeCount(count) {
    writeDigit(0, getDigit((count>>4)&0xf));
    writeDigit(1, getDigit(count&0xf));
}

function getDigit(ch) {
    var segs;
    switch(ch) {
        case 0:
            segs = 0b0111111;
            break;
        case 1:
            segs = 0b0000110;
            break;
        case 2:
            segs = 0b1011011;
            break;
        case 3:
            segs = 0b1001111;
            break;
        case 4:
            segs = 0b1100110;
            break;
        case 5:
            segs = 0b1101101;
            break;
        case 6:
            segs = 0b1111101;
            break;
        case 7:
            segs = 0b0000111;
            break;
        case 8:
            segs = 0b1111111;
            break;
        case 9:
            segs = 0b1101111;
            break;
        case 0xa:
        case 'a':
            segs = 0b1110111;
            break;
        case 0xb:
        case 'b':
            segs = 0b1111100;
            break;
        case 0xc:
        case 'c':
            segs = 0b0111001;
            break;
        case 0xd:
        case 'd':
            segs = 0b1011110;
            break;
        case 0xe:
        case 'e':
            segs = 0b1111001;
            break;
        case 0xf:
        case 'f':
            segs = 0b1110001;
            break;
        case 'g':
            segs = 0b0000000;
            break;
        case 'h':
            segs = 0b1010101;
            break;
        case 'i':
            segs = 0b0101010;
            break;
        default:
            segs = 0;
            break;
    }

    return segs;
}

function writeDigit(digit, segs) {
    var index = digit * 8;
    var seg;
    for(var i = 0; i < 7; i++) {
        seg = (segs >> i) & 1;
        b.writeTextFile("/sys/class/leds/techlab::seg" + (index+i) + "/brightness", seg);
    }
}