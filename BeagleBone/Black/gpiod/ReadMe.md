libgpiod is a new C library and tools for interacting with the linux GPIO
character device. 
Detailed information is 
[here](https://git.kernel.org/pub/scm/libs/libgpiod/libgpiod.git/tree/README)
and [Adafruit](https://blog.adafruit.com/2018/11/26/sysfs-is-dead-long-live-libgpiod-libgpiod-for-linux-circuitpython/)
also has information.

One of the advantages of gpiod is that it can toggle multiple bits on the same
gpio chip at the same time.  The toggle2 examples show how it's done.

The directory contains examples of using gpiod with **C** and **python** to read/write
a gpio pin.

File                | Description
----                | -----------
[toggle1](toggle1.c)    | Toggles one pin as fast as possible.  (300KHz in C, 57KHz in python)
[toggle2](toggle2.c)    | Toggles two pins as fast as possible.  (280KHz in C, 55KHz in python)
[get](get.c)    | Reads an input pin and prints its value.
[getset](getset.c)    | Reads an input pin and writes its value to an output pin. (5us delay in C, 20 us Delay in python)
[getsetEvent](getset.c)    | Like **getset**, but uses events. (40 us delay in C, 75 us delay in python)
[toggleLED](toggleLED.c)    | Toggles the four built in USR LEDs.

> Tip:  Use **gpioinfo** to lookup chip and line numbers for various pins.
