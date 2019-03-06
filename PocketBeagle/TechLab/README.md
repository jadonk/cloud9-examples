# TechLab

## Setup microSD card

Use https://rcn-ee.net/rootfs/bb.org/testing/2019-03-03/buster-iot/bone-debian-buster-iot-armhf-2019-03-03-4gb.img.xz image or newer

## Login

Use Cloud9 IDE or serial terminal

user: debian<br>
password: temppwd

## Install overlays

There are instructions below for working both with and without overlays. It all depends on what you want to learn.

Without overlays, you'll be using userspace interfaces to the bus controllers and doing parts of what the Linux drivers
do for you.

With overlays, you'll be looking at interfaces provided by relatively complete drivers. You can then start learning
about how those drivers are built and configured, once you understand how to use them. They often expose interesting
features of the Linux kernel.

```
sudo sed -i -e "s/#?uboot_overlay_addr0=.*$/uboot_overlay_pru=\/lib\/firmware\/PB-I2C2-ACCEL-TECHLAB-CAPE.dtbo/;" /boot/uEnv.txt
sudo sed -i -e "s/#?uboot_overlay_addr1=.*$/uboot_overlay_pru=\/lib\/firmware\/PB-PWM-RGB-TECHLAB-CAPE.dtbo/;" /boot/uEnv.txt
sudo sed -i -e "s/#?uboot_overlay_addr2=.*$/uboot_overlay_pru=\/lib\/firmware\/PB-SPI1-7SEG-TECHLAB-CAPE.dtbo/;" /boot/uEnv.txt
sudo sed -i -e "s/#?uboot_overlay_pru=.*RPROC.*$/uboot_overlay_pru=\/lib\/firmware\/AM335X-PRU-RPROC-4-14-TI-00A0.dtbo/;" /boot/uEnv.txt
sudo shutdown -r now
```

## Verify configuration

```
sudo /opt/scripts/tools/version.sh
```

# Testing interfaces

## Buttons
* L (only user button on BaconBits)
	* Pin: P2_33
	* Ball: R12
	* GPIO: 45
* R
	* Pin: P1_29
	* Ball: A14
	* GPIO: 117
	* PRU: PRU0_7

```
config-pin p1.29 gpio
cd /sys/class/gpio;watch -n0 cat gpio45/value gpio117/value
```

## Light sensor (Potentiometer on BaconBits)

The ADC driver is always assumed to be loaded.

* Pin: P1_19
* Ball: B6
* AIN: 0

```
watch -n0 cat /sys/bus/iio/devices/iio\:device0/in_voltage0_raw
```

## I2C Accelerometer
* Bus: I2C2
* Device: mma8453
* Pins:
	* SDA: P1_26
	* SCL: P1_28
	* INT1: P1_34
	* INT2: P1_33
	* Addr: 0x1c

### No overlay

```
i2cset -y 2 0x1c 0x2a 1
watch -n0 i2cdump -y -r 1-6 2 0x1c
```

### Loading configfs overlay

This requires the device-tree configfs interface to be enabled. Once you run this, you
can follow it up by running the "with overlay" example.

```
sudo mkdir -p /sys/kernel/config/device-tree/overlays/accel
sudo dtc -W no-unit_address_vs_reg -@ -o /sys/kernel/config/device-tree/overlays/accel/dtbo <<EOF
/dts-v1/;
/plugin/;
/ {
	fragment@0 {
		target = <&i2c2>;
		__overlay__ {
			#address-cells = <1>;
			#size-cells = <0>;
			accel@1c {
				compatible = "fsl,mma8453";
				reg = <0x1c>;
			};
		};
	};
};
EOF
sleep 2
```

### With overlay

```
cd /sys/bus/iio/devices/iio\:device1;watch -n0 cat in_accel_x_raw in_accel_y_raw in_accel_z_raw                                                                                                
```

## SPI 7-segment LEDs

Either the spidev driver or full 

* Bus: SPI1
* Device: 
* Pins:
	* SCLK: P2_29
	* CS1: P2_31
	* MOSI: P2_25
	* MISO: P2_27

### Userspace spidev interface

The device might be named spidev1.1 or spidev2.1, depending on the
kernel version and device tree used with your kernel.  The easiest way
to know is to look at ```/sys/devices/platform/ocp/481a0000.spi/spi_master/```
and see if it says spi1 or spi2. REplace SPIDEV below accordingly.

```
export SPIDEV=/dev/spidev1.1
echo -ne "\x40\x00\x00" | sudo tee $SPIDEV | xxd
echo -ne "\x40\x01\x00" | sudo tee $SPIDEV | xxd
echo -ne "\x40\x12\xc0" | sudo tee $SPIDEV | xxd
echo -ne "\x40\x13\xc0" | sudo tee $SPIDEV | xxd
```

### With overlay

```
echo 1 > /sys/class/leds/techlab\:\:seg0/brightness
echo 1 > /sys/class/leds/techlab\:\:seg1/brightness
echo 1 > /sys/class/leds/techlab\:\:seg2/brightness
echo 1 > /sys/class/leds/techlab\:\:seg3/brightness
echo 1 > /sys/class/leds/techlab\:\:seg4/brightness
echo 1 > /sys/class/leds/techlab\:\:seg5/brightness
echo 1 > /sys/class/leds/techlab\:\:seg6/brightness
echo 1 > /sys/class/leds/techlab\:\:seg8/brightness
echo 1 > /sys/class/leds/techlab\:\:seg9/brightness
echo 1 > /sys/class/leds/techlab\:\:seg10/brightness
echo 1 > /sys/class/leds/techlab\:\:seg11/brightness
echo 1 > /sys/class/leds/techlab\:\:seg12/brightness
echo 1 > /sys/class/leds/techlab\:\:seg13/brightness
echo 1 > /sys/class/leds/techlab\:\:seg14/brightness
```

## PWM RGB LED
* Red
	* Pin: P1_33
	* PWM: EHRPWM0B
	* PRU: PRU0_1
* Green
	* Pin: P2_1
	* PWM: EHRPWM1A
* Blue
	* Pin: P1_36
	* PWM: EHRPWM0A


### Without overlay

TBD

### With overlay

```
config-pin p1.33 pwm
echo 10 | sudo tee /sys/class/leds/techlab\:\:red/brightness
echo 10 | sudo tee /sys/class/leds/techlab\:\:green/brightness
echo 10 | sudo tee /sys/class/leds/techlab\:\:blue/brightness
```

## PRU Buzzer

Requires PRU0 firmware image from beagle-tester. Needs to be put into the bone101 demos.

```
#echo pruout > /sys/devices/platform/ocp/ocp\:P2_30_pinmux/state
config-pin p2.30 pruout
echo stop | sudo tee /sys/class/remoteproc/remoteproc1/state
echo start | sudo tee /sys/class/remoteproc/remoteproc1/state
```

## mikroBUS (not on BaconBits)

| Left               | Right             |
|--------------------|-------------------|
| AIN6/GPIO87 (P1_2) | PWM1A (P2_1) **   |
| INT/GPIO89 (P1_4)  | RST/GPIO23 (P2_3) |
| SPI0 CS (P1_6)     | UART4 RX (P2_5)   |
| SPI0 CLK (P1_8)    | UART4 TX (P2_7)   |
| SPI0 MISO (P1_10)  | I2C1 SCL (P2_9)   |
| SPI0 MOSI (P1_12)  | I2C1 SDA (P2_11)  |
| +5V/VOUT           | +3.3V             |
| GND                | GND               |

* ** PWM1A (P2_1) is shared with the green of the RGB LED.

## To do

```
echo 10 > /sys/class/leds/techlab\:\:green/brightness
echo 100 > /sys/class/leds/techlab\:\:blue/brightness
echo pwm > /sys/devices/platform/ocp/ocp\:P1_33_pinmux/state
echo 200 > /sys/class/leds/techlab\:\:red/brightness
echo 1 > /sys/class/leds/techlab\:\:seg0/brightness
echo 1 > /sys/class/leds/techlab\:\:seg1/brightness
echo 1 > /sys/class/leds/techlab\:\:seg2/brightness
echo 1 > /sys/class/leds/techlab\:\:seg3/brightness
echo 1 > /sys/class/leds/techlab\:\:seg4/brightness
echo 1 > /sys/class/leds/techlab\:\:seg5/brightness
echo 1 > /sys/class/leds/techlab\:\:seg6/brightness
echo 1 > /sys/class/leds/techlab\:\:seg8/brightness
echo 1 > /sys/class/leds/techlab\:\:seg9/brightness
echo 1 > /sys/class/leds/techlab\:\:seg10/brightness
echo 1 > /sys/class/leds/techlab\:\:seg11/brightness
echo 1 > /sys/class/leds/techlab\:\:seg12/brightness
echo 1 > /sys/class/leds/techlab\:\:seg13/brightness
echo 1 > /sys/class/leds/techlab\:\:seg14/brightness
echo pruout > /sys/devices/platform/ocp/ocp\:P2_30_pinmux/state
echo start > /sys/class/remoteproc/remoteproc1/state
echo stop > /sys/class/remoteproc/remoteproc1/state
echo start > /sys/class/remoteproc/remoteproc1/state
cat /sys/bus/iio/devices/iio\:device0/in_voltage0_raw
cat /sys/bus/iio/devices/iio\:device0/in_voltage0_raw
cat /sys/bus/iio/devices/iio\:device1/in_accel_x_raw
cat /sys/bus/iio/devices/iio\:device1/in_accel_x_raw
cat /sys/bus/iio/devices/iio\:device1/in_accel_x_raw
echo gpio > /sys/class/leds/techlab\:\:seg0/trigger
echo 45 > /sys/class/leds/techlab\:\:seg0/gpio
echo 1 > /sys/class/leds/techlab\:\:seg0/inverted
cat /sys/class/leds/techlab\:\:seg0/brightness
cat /sys/class/leds/techlab\:\:seg0/brightness
echo gpio > /sys/devices/platform/ocp/ocp\:P1_29_pinmux/state
echo gpio > /sys/class/leds/techlab\:\:seg1/trigger
echo 117 > /sys/class/leds/techlab\:\:seg1/gpio
echo 1 > /sys/class/leds/techlab\:\:seg1/inverted
cat /sys/class/leds/techlab\:\:seg1/brightness
cat /sys/class/leds/techlab\:\:seg1/brightness
```

## Version info for examples
```
debian@beaglebone:/var/lib/cloud9$ sudo /opt/scripts/tools/version.sh
[sudo] password for debian:
git:/opt/scripts/:[1aa73453b2c980b75e31e83dab7dd8b6696f10c7]
eeprom:[A335PBGL00A21741GPB42934]
model:[TI_AM335x_PocketBeagle]
dogtag:[BeagleBoard.org Debian Image 2018-10-07]
bootloader:[microSD]:[/dev/mmcblk0]:[U-Boot 2018.09-00002-g0b54a51eee]:[location: dd MBR]
kernel:[4.14.71-ti-r80]
nodejs:[v6.14.4]
uboot_overlay_options:[enable_uboot_overlays=1]
uboot_overlay_options:[uboot_overlay_addr0=/lib/firmware/PB-I2C2-ACCEL-TECHLAB-CAPE.dtbo]
uboot_overlay_options:[uboot_overlay_addr1=/lib/firmware/PB-PWM-RGB-TECHLAB-CAPE.dtbo]
uboot_overlay_options:[uboot_overlay_addr2=/lib/firmware/PB-SPI1-7SEG-TECHLAB-CAPE.dtbo]
uboot_overlay_options:[uboot_overlay_pru=/lib/firmware/AM335X-PRU-RPROC-4-14-TI-00A0.dtbo]
uboot_overlay_options:[enable_uboot_cape_universal=1]
pkg check: to individually upgrade run: [sudo apt install --only-upgrade <pkg>]
pkg:[bb-cape-overlays]:[4.4.20180928.0-0rcnee0~stretch+20180928]
pkg:[bb-wl18xx-firmware]:[1.20180517-0rcnee0~stretch+20180517]
pkg:[kmod]:[23-2rcnee1~stretch+20171005]
pkg:[librobotcontrol]:[1.0.3-git20181005.0-0rcnee0~stretch+20181005]
pkg:[firmware-ti-connectivity]:[20170823-1rcnee1~stretch+20180328]
groups:[debian : debian adm kmem dialout cdrom floppy audio dip video plugdev users systemd-journal i2c bluetooth netdev cloud9ide gpio pwm eqep admin spi tisdk weston-launch xenomai]
cmdline:[console=ttyO0,115200n8 bone_capemgr.uboot_capemgr_enabled=1 root=/dev/mmcblk0p1 ro rootfstype=ext4 rootwait coherent_pool=1M net.ifnames=0 quiet]
dmesg | grep pinctrl-single
[    1.079830] pinctrl-single 44e10800.pinmux: 142 pins at pa f9e10800 size 568
dmesg | grep gpio-of-helper
[    1.088027] gpio-of-helper ocp:cape-universal: ready
END
```
