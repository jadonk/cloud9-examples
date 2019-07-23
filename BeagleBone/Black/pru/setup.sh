#!/bin/bash
export MODEL=$(awk '{print $NF}' /proc/device-tree/model)
if [ $MODEL != "AI" ]; then
    export PRUN=0
else
    export PRUN=1_1
fi

export TARGET=blinkInternalLED

echo PRUN=$PRUN
echo TARGET=$TARGET
echo MODEL=$MODEL

echo none > /sys/class/leds/beaglebone\:green\:usr1/trigger
echo none > /sys/class/leds/beaglebone\:green\:usr2/trigger
