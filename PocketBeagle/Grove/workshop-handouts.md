# PocketBeagle Grove Kit Hands-On Coding Workshop

* microSD software image and other materials available from bbb.io/grove

See bbb.io/start for instructions on using Etcher.io to write a microSD card

TODO: Add image for getting-started web page

TOOD: Determine if all wires should be hooked up in this phase.

Plug into the microUSB on PocketBeagle to provide power and a network connection. Look for the “heartbeat” pulse on the USR0 LED to know the board has Linux up-and-running.

TODO: Add image for power connection to PocketBeagle

## Get to the Cloud9 IDE
Windows: http://192.168.7.2  
Linux/Mac: http://192.168.6.2

TODO: Move to a single server type supported by latest Windows and Mac

TODO: Add image of Cloud9 IDE startup

----

# PocketBeagle Grove Kit

TODO: Add image of kit

# PocketBeagle Grove Kit wiring summary

TOOD: Document interconnections

----

# PocketBeagle

TODO: add image of PocketBeagle

* PocketBeagle® is an ultra-tiny-yet-complete, low-cost, open-source USB-key-fob computer. 
* Processor System:  Octavo Systems OSD3358-SM 21mm x 21mm system-in-package that includes 512MB DDR3 RAM, 1-GHz ARM Cortex-A8 CPU, 2x 200-MHz PRUs, ARM Cortex-M3, 3D accelerator, power/battery management and EEPROM
* 72 expansion pin headers with power and battery I/Os, high-speed USB, 8 analog inputs, 44 digital I/Os and numerous digital interface peripherals
* microUSB host/client and microSD connectors

## PocketBeagle Expansion Header Pin-out

TODO: add image of PocketBeagle expansion header

Great getting started information is at beagleboard.org/pocket

----

# Blink PocketBeagle on-board USRx LED
**Goal:** Blink USR3 LED on PocketBeagle

**Overview:** Python is a popular programming language used by beginners. Linux exposes hardware interfaces as files, making it easy to use any programming language to interact with hardware. Here we will use Python and Linux to blink an LED built into your PocketBeagle.

**Do this in the Cloud9 IDE:**

1. Navigate to *PocketBeagle/Grove/internalLED.py* and double-click on it.
2. Click the ```Run``` button in the toolbar to execute the script in the ```active file window```.
3. You will see the ```run configuration window``` open with a ```Stop``` button.  Click the ```Stop``` button to halt the program.
4. Try changing the LED or blink time, save the program and run again.

TODO: Add image of Cloud9 IDE.

## internalLED.py

```
#!/usr/bin/env python3
import time
state = 0 # Initial state
led = open('/sys/class/leds/beaglebone:green:usr3/brightness', 'w')
while True:
  print(state, file=led)
  led.flush()
  if(state == 1):
    state = 0
  else:
    state = 1
  time.sleep(0.25)
```

----

