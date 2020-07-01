#!/usr/bin/python3
#//////////////////////////////////////
#	counter.py
#	Uses 7-segment LEDs to count up and down with presses of R and L.
#//////////////////////////////////////
import Adafruit_BBIO.GPIO as GPIO
import time

L_BUTTON = "P2_33"
R_BUTTON = "P1_29"
GPIO.setup(L_BUTTON, GPIO.IN)
GPIO.setup(R_BUTTON, GPIO.IN)

# Need to add:  debounce

def writeCount(count):
    writeDigit(0, getDigit((count>>4)&0xf))
    writeDigit(1, getDigit(count&0xf))

def getDigit(ch):
    switcher = {
        0:  0b0111111,
        1:  0b0000110,
        2:  0b1011011,
        3:  0b1001111,
        4:  0b1100110,
        5:  0b1101101,
        6:  0b1111101,
        7:  0b0000111,
        8:  0b1111111,
        9:  0b1101111,
        0xa: 0b1110111,
        'a': 0b1110111,
        0xb: 0b1111100,
        'b': 0b1111100,
        0xc: 0b0111001,
        'c': 0b0111001,
        0xd: 0b1011110,
        'd': 0b1011110,
        0xe: 0b1111001,
        'e': 0b1111001,
        0xf: 0b1110001,
        'f': 0b1110001
    }
    return switcher.get(ch, "Invalid month")


def writeDigit(digit, segs):
    index = digit * 8;
    for i in range(8):
        seg = (segs >> i) & 1
        fd = open("/sys/class/leds/techlab::seg" + str(index+i) + "/brightness", 'w') 
        fd.write(str(seg)) 
        fd.close()

counter = 0

def onPress(x):
    global counter
    # print('onPress: ' + x)
    if x == L_BUTTON:
        counter = counter - 1
        if counter<0:
            counter = 0
    if x == R_BUTTON:
        counter = counter + 1
        if counter>0xff:
            counter = 0xff
    print('counter: ' + str(counter))
    writeCount(counter)

GPIO.add_event_detect(L_BUTTON, GPIO.RISING, callback=onPress)
GPIO.add_event_detect(R_BUTTON, GPIO.RISING, callback=onPress)

print('Hit ^C to exit');
while True:
    time.sleep(100)
