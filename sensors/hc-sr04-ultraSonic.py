#!/usr/bin/env python3

# // This is an example of reading HC-SR04 Ultrasonic Range Finder
# // This version measures from the fall of the Trigger pulse 
# //   to the end of the Echo pulse

import Adafruit_BBIO.GPIO as GPIO
# import GPIOmay as GPIO
import time

trigger = 'P9_15'  # Pin to trigger the ultrasonic pulse
echo    = 'P9_13'    # Pin to measure to pulse width related to the distance
ms = 2500            # Trigger period in ms

GPIO.setup(trigger, GPIO.OUT)

GPIO.setup(echo, GPIO.IN)

startTime = 0       # Make it global

def pingEnd(channel):
    global startTime
    # print('Edge detected on channel %s'%channel)
    totalTime = time.perf_counter() - startTime
    print('totalTime = ' + str(2000/2.7*totalTime))
    # startTime = time.perf_counter()

GPIO.add_event_detect(echo, GPIO.FALLING, callback=pingEnd) 

# Pull trigger low and start timing.
while True:             # Do something while waiting for event
    # print('ping')
    GPIO.output(trigger, 1)
    startTime = time.perf_counter()
    time.sleep(0.005)
    GPIO.output(trigger, 0)
    time.sleep(1)
    
GPIO.cleanup()


# var startTime, pulseTime;
    
# b.pinMode(echo,    b.INPUT);
# b.pinMode(trigger, b.OUTPUT);

# b.attachInterrupt(echo, pingEnd, b.both);
 
# b.digitalWrite(trigger, 1);     // Unit triggers on a falling edge.
#                                 // Set trigger to high so we call pull it low later

# // Pull the trigger low at a regular interval.
# setInterval(ping, ms);

# // Pull trigger low and start timing.
# function ping() {
#     console.log('ping');
#     b.digitalWrite(trigger, 0);
#     startTime = process.hrtime();
#     console.log(b.digitalRead(echo))
# }

# // Compute the total time and get ready to trigger again.
# function pingEnd(x) {
#     // console.log("x: ", util.inspect(x));
#     if(x.attached) {
#         console.log("Interrupt handler attached: " + x.pin.key);
#         return;
#     }
#     // if(startTime) {
#         pulseTime = process.hrtime(startTime);
#         b.digitalWrite(trigger, 1);
#         console.log('pulseTime = ' + (pulseTime[1]/1000000-0.8).toFixed(3));
#     // }
# }
