#!/bin/bash

export TARGET=blinkInternalLED.pru0

echo TARGET=$TARGET

echo none > /sys/class/leds/beaglebone\:green\:usr1/trigger
echo none > /sys/class/leds/beaglebone\:green\:usr2/trigger
