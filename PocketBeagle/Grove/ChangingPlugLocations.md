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
Switching plugs often means editing a device tree.  Fortunatley the source code
for the device trees is already on the PocketBeagle.  Just do the following:
```bash
bone$ cd /opt/source/bb.org-overlays
bone$ ls src/arm
````
Here you will find nearly 250 device trees.  Which ones do we need to edit? Try:
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

The following table lists which device tree is for which device.

|Tree    | Interface | Description |
|--------| --------- |-------------|
|PB-I2C1-TLV320AIC3104.dts | I2C  | The audio speaker
|BB-GPIO-P9813.dts          | GPIO | The LED
|BB-GPIO-HCSR04.dts         | GPIO | The ultrasonic range finder
|BB-GPIO-GROVE-BUTTON.dts   | GPIO | The push button
|BB-I2C1-JHD1802.dts        | I2C  | The LCD
|BB-I2C2-ADXL34X.dts        | I2C  | The accelerometer
|BB-I2C2-MPR121.dts         | I2C  | The capative touch sensor

## Examples

### Accelerometer - I2C
The accelerometer is set for I2C**2**.  Let's move it to I2C**1**.  

#### Device tree
Find the device and make a copy of it.
```bash
bone$ cd /opt/source/bb.org-overlays/src/arm
bone$ cp BB-I2C2-ADXL34X.dts BB-I2C1-ADXL34X.dts
```
Edit the newly created file.  Around line 30 you'll find:
```bash
			aliases {
				/* SLOT I2C1 */
				/*
				adxl345 = "/ocp/i2c@4802a000/adxl345@53";
				*/
				/* SLOT I2C2 */
				adxl345 = "/ocp/i2c@4819c000/adxl345@53";
			};
```
Uncomment the I2C1 entry and comment out th I2C2 entery:
```bash
			aliases {
				/* SLOT I2C1 */
				
				adxl345 = "/ocp/i2c@4802a000/adxl345@53";
				
				/* SLOT I2C2 */
				// adxl345 = "/ocp/i2c@4819c000/adxl345@53";
			};
```
Then go down to line 42 and do it again:
```bash
	fragment@2 {
		/* SLOT I2C1 */
		
		target = <&i2c1>;
		
		/* SLOT I2C2 */
		// target = <&i2c2>;
```
Next, make the device tree
```bash
bone$ cd /opt/source/bb.org-overlays
bone$ make
  DTC     src/arm/BB-I2C1-ADXL34X.dtbo
gcc -o config-pin ./tools/pmunts_muntsos/config-pin.c
bone$ sudo make install
...
```
Notice it finds the new file and compiles it.

#### uEnv.txt
Next, edit `/boot/uEnt.txt`.  Around line 69 change the old filename to the new filename.
```bash
uboot_overlay_addr5=/lib/firmware/BB-I2C1-ADXL34X.dtbo
```
Plug the accelerometer into I2C**1** and reboot.
```bash
bone$ sudo reboot
```
Once the bone has rebooted, run Accelerometer.py to test that it's switched.
```bash
bone$ cd /var/lib/cloud9/PocketBeagle/Grove/
bone$ ./Accelerometer.py
[35, 0, 54]
[35, 0, 54]
[36, 0, 53]
```


### Buttons - GPIO
By default the buttons in the Grove Kit plug into **A5** and **UART4**.  It's not hard to move them to the other plus.  Suppose you would like a button on UART**0**.  The table above shows the buttons are interfaced via GPIO and 
*BB-GPIO-GROVE-BUTTON.dts*.

```bash
bone$ cd /opt/source/bb.org-overlays
```
Then edit `src/arm/BB-GPIO-GROVE-BUTTON.dts` around line 96 you'll see:
```bash
				grove_button_1057_0@0 {
					debounce_interval = <50>;
					linux,code = <0x100>;
					label = "grove:usr0";
					/* Grove Button, HIGH valid/press */
					gpios = <&gpio0 30 0x0>;
					gpio-key,wakeup;
					autorepeat;
				};
```
This says what GPIO 0_30 is where the button is attached. Search the P2 headers
file (noted above) for **0_30** and you'll find:
```bash
Header.Pin	Silkscreen	PocketBeagle wiring	Proc Ball	SiP Ball	Mode0 (Name)	Mode1	Mode2	Mode3	Mode4	Mode5	Mode6	Mode7													
P2.05	U1_RX	P2.05 (UART4-RX)	T17	P15	gpmc_wait0	gmii2_crs	gpmc_csn4	rmii2_crs_dv	mmc1_sdcd	pr1_mii1_col	uart4_rxd	gpio0_30													
```
This shows that GPIO 0_33 is attached to the headers P2.05 which is UART4-RX.
That confirms what we already new, the button is attached to the UART4-RX.
We want to connect to UART0-RX, so search the P2 header file for UART**0**-RX.
```bash
Header.Pin	Silkscreen	PocketBeagle wiring	Proc Ball	SiP Ball	Mode0 (Name)	Mode1	Mode2	Mode3	Mode4	Mode5	Mode6	Mode7													
P1.32	U0_RX	P1.32 (UART0-RX)	E15	A12	uart0_rxd	spi1_cs0	dcan0_tx	I2C2_SDA	eCAP2_in_PWM2_out	pr1_pru1_pru_r30_14	pr1_pru1_pru_r31_14	gpio1_10
```
Here we see it's attached to P1.32 which is GPIO 1_10 (rightmost column).  
Edit the device tree so *gpios* is gpio1 10 as shown.
```bash
				grove_button_1057_0@0 {
					debounce_interval = <50>;
					linux,code = <0x100>;
					label = "grove:usr0";
					/* Grove Button, HIGH valid/press */
					// gpios = <&gpio0 30 0x0>;
					gpios = <&gpio1 10 0x0>;
					gpio-key,wakeup;
					autorepeat;
				};
```
Now move the UART4 button to UART0 and reboot.
```bash
bone$ cd /opt/source/bb.org-overlays
bone$ make
bone$ sudo make install
bone$ sudo reboot
```
Once the bone reboots, run Button.py and it should work with the button
plugged into UART0.

## Summary
It was shown how to switch I2C buses and GPIO pins for the accelerometer and
the buttons.  This approach generalizes to other GPIO and I2C devices as well.
