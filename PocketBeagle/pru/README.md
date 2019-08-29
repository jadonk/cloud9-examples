This folder contains demos of the BeagleBone's PRU (Programable Real-time Unit)
The PRUs have 32-bit cores which run independently of the ARM processor, 
therefore they can be programmed to respond quickly to inputs and produce 
very precisely timed outputs.

There are many projects that use the PRU 
(http://processors.wiki.ti.com/index.php/PRU_Projects) 
to do things that can’t be done with just a SBC or just a microcontroller.

Here we demonstrate:
```
blinkInternalLED.c  // Blink some of the built in USR LEDs
blinkExternalLED.c  // Wire an external LED and blink it
blinkR31.c          // Blink and external LED using a faster (50MHz) method

neopixelStatic.c    // Wire up NeoPixel (WS2812) LEDs and set them to a color
neopixelDynamic.c   // Same LEDs, but a moving display
neopixelRpmsg.c     // Control the NeoPixels from the ARM using rpmsg for message passing
neopixelRainbow.py      // Runs on the ARM and writes a rainbow pattern to the PRU

inputR31.c          // Reads an input pin via the fast R31 register
bitflip.c           // Shows how to share memory between the ARM and the PRU

ring.c              // Does the "Ring Test" to see how quickly I/O can be toggled
```
The Pocket has two PRUs, pru0 and pru1.

The filename tells which PRU to run on.  For example blinkInternalLED.pru0.c will
run on pru0.  These demos must all run on pru0, except blinkInternalLED, which
can run on ether of the PRUs.  