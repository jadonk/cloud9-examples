## Changing Plug Locations

The PocketBeagle Groove kit comes with many sensors and devices that are plugged
into the PocketBeagle Groove Cape using various interfaces such as I2C and
the GPIO pins.  For example the *3 Axis Digital Accelerometer*
plugs into the I2C bus where the *Buttons* use GPIO.  

The examples given show how to plug one device into one location.  For example,
the Accelerometer is show plugging into I2C**2**.  

The purpose of these instructions is to show how to adjust the code so the
devices can be plugged in in other locations.  For example plugging the
Accelerometer in to I2C**1**.  

First, some background.

### Device tree source code 
Switching plugs often means editting a device tree.  Fortunatley the source code
for the device trees is already on the PocketBeagle.  Just do the following:
```bash
bone$ cd /opt/source/bb.org-overlays
bone$ ls src/arm
````
Here you will find nearly 500 device trees.  Which ones do wee need to edit? Try:
``` bash
bone$ grep firmware /boot/uEnv.txt
uboot_overlay_addr0=/lib/firmware/PB-I2C1-TLV320AIC3104.dtbo
uboot_overlay_addr1=/lib/firmware/BB-GPIO-P9813.dtbo
uboot_overlay_addr2=/lib/firmware/BB-GPIO-HCSR04.dtbo
uboot_overlay_addr3=/lib/firmware/BB-GPIO-GROVE-BUTTON.dtbo
uboot_overlay_addr4=/lib/firmware/BB-I2C1-JHD1802.dtbo
uboot_overlay_addr5=/lib/firmware/BB-I2C2-ADXL34X.dtbo
uboot_overlay_addr6=/lib/firmware/BB-I2C2-MPR121.dtbo
```
These are the seven device trees that are loaded by default.  First let's *make* 
and install everyting before we change anything.  This will take about 
a minute on the bone.
```bash
bone$ make
  DTC     src/arm/PB-I2C1-TLV320AIC3104.dtbo
  DTC     src/arm/BB-I2C1-00A0.dtbo
...
  DTC     src/arm/PB-eqep2.dtbo
  DTC     src/arm/PB-MCP2515-SPI1.dtbo
gcc -o config-pin ./tools/pmunts_muntsos/config-pin.c
```
```bash
bone$ sudo make install
mkdir -p /lib/firmware/
cp -v src/arm/*.dtbo /lib/firmware/
'src/arm/ACME-revB.dtbo' -> '/lib/firmware/ACME-revB.dtbo'
'src/arm/AM335X-20-00A0.dtbo' -> '/lib/firmware/AM335X-20-00A0.dtbo'
'src/arm/AM335X-I2C1-400-00A0.dtbo' -> '/lib/firmware/AM335X-I2C1-400-00A0.dtbo'
's
...
'src/arm/uio_pruss_enable-00A0.dtbo' -> '/lib/firmware/uio_pruss_enable-00A0.dtbo'
mkdir -p /usr/bin/
cp -v config-pin /usr/bin/
'config-pin' -> '/usr/bin/config-pin'
```
Now that we know everything compiles, let's look up how things are connected.

### P1 and P2 Headers
The PocketBeagle has two headers, labeled **P1** and **P2**.  The 
[System Reference Manual](https://github.com/beagleboard/pocketbeagle/wiki/System-Reference-Manual) 
shows what connects to the various pins. Here's the 
[P1 Table](https://github.com/beagleboard/pocketbeagle/wiki/System-Reference-Manual#711_P1_Header)
and the
[P2 Table](https://github.com/beagleboard/pocketbeagle/wiki/System-Reference-Manual#712_P2_Header).

Easier to use tables are [here](https://docs.google.com/spreadsheets/d/1FRGvYOyW1RiNSEVprvstfJAVeapnASgDXHtxeDOjgqw/edit#gid=0).

### Mapping Device Tree to Devices

The following table list which device tree is for which device.

|Tree    | Interface | Description |
|--------| --------- |-------------|
|PB-I2C1-TLV320AIC3104.dtbo | I2C  | The audio speaker
BB-GPIO-P9813.dtbo          | GPIO | The LED
BB-GPIO-HCSR04.dtbo         | GPIO | The ultrasonic range finder
BB-GPIO-GROVE-BUTTON.dtbo   | GPIO | The push button
BB-I2C1-JHD1802.dtbo        | I2C  | The LCD
BB-I2C2-ADXL34X.dtbo        | I2C  | The accelerometer
BB-I2C2-MPR121.dtbo         | I2C  | The capative touch sensor

## Examples

### Accelerometer 
The accelerometer is set for I2C**2**.  Let's move it to I2C**1**.  

#### Device tree
Find the device and make a copy of it.
```bash
bone$ cd /opt/source/bb.org-overlays/src/arm
bone$ cp BB-I2C2-ADXL34X.dts BB-I2C1-ADXL34X.dts
```
