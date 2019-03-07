# Grove modules

This is a set of examples for using Seeed Grove modules with PocketBeagle, primarily using
the BeagleBoard.org PocketBeagle Grove Cape, but some other wiring options are examined as
well.

# BeagleBoard.org PocketBeagle Grove Cape

| Grove socket and pin | PocketBeagle pin(s) |
| --- | --- |
| I2C1 - 1 | ```P2_9``` (I2C1) |
| I2C1 - 2 | ```P2_11``` (I2C1) |
| I2C2 - 1 | ```P1_28``` (I2C2) |
| I2C1 - 2 | ```P1_26``` (I2C0) |
| UART4 - 1 | ```P2_5``` (UART4) |
| UART4 - 2 | ```P2_7``` (UART4) |
| IO59 - 1 | ```P1_32``` (UART0) ```P2_2``` (GPIO59) ** |
| IO59 - 2 | ```P1_30``` (UART0) ```P2_8``` (GPIO60) ** |
| IO57 - 1 | ```P2_6``` (GPIO57) ** |
| IO57 - 2 | ```P2_4``` (GPIO58) ** |
| A0 - 1 | ```P1_19``` (AIN0) ```P1_33``` (PRU0.1) |
| A0 - 2 | ```P1_21``` (AIN1) ```P2_32``` (PRU0.2) |
| A2 - 1 | ```P1_23``` (AIN2) ```P2_30``` (PRU0.3) |
| A2 - 2 | ```P1_25``` (AIN3) ```P1_31``` (PRU0.4) |
| PWM - 1 | ```P1_36``` (PWM0A) |
| PWM - 2 | ```P2_1``` (PWM1A) |

* ** Try to avoid using these signals as they are likely to change on future revisions.

## I2C1/I2C2

To use these ports as 3.3V I2C, the default configuration should be ready-to-go. Depending
on the sensor you are using, you'll simply need to enable the kernel driver and interact
using the newly created SYSFS entries. This is easy and can be quickly learned by example.

Take the [Grove time of flight distance sensor](http://wiki.seeedstudio.com/Grove-Time_of_Flight_Distance_Sensor-VL53L0X/)
as a first example. As long as the kernel is new enough or the module is installed, you'll
simply need to write to a file called ```/sys/bus/i2c_devices/i2c-2/new_device``` to
trigger the loading of the driver, assuming you've connected it to I2C2. Swap i2c-2 with
i2c-1 if you've connected it to I2C1. What you'll need to write is the string ```vl53l0x 0x29```.
This is the device driver name and the I2C address of the device on the Grove module.

In this directory, you'll find numerous examples in various programming languages to
perform this task, but you can also simply do everything necessary from the Linux
command shell. You'll see the shell in your Cloud9 IDE window as 'bash'. Simply type
in these two lines to read from the time of flight sensor.

```sh
echo vl53l0x 0x29 | sudo tee /sys/bus/i2c/devices/i2c-2/new_device
cat /sys/bus/iio/devices/iio\:device1/in_distance_raw
```

The first line loads the driver and the second line reads the sensor. If you have more
sensor drivers loaded, the ```iio:device1``` might be incremented to ```iio:device2```
or whatever the next available index is.

To read it continuously, you can do something like:

```sh
watch -n0 cat /sys/bus/iio/devices/iio\:device1/in_distance_raw
```

The summary of SYSFS entries (virtual files) providing an interface to the module are
documented at https://www.kernel.org/doc/Documentation/ABI/testing/sysfs-bus-iio.  You
should look for the interfaces typical for the type of sensor.

The following table provides a summary of I2C sensors, the name of the driver, the
default I2C address, and the minimal kernel revision to support the sensor. The kernel
version also includes a link to the kernel module source code.

| Module name and wiki link | Driver name and I2C address | Kernel version and link to driver source |
| --- | --- | --- |
| [Digital light sensor](http://wiki.seeed.cc/Grove-Digital_Light_Sensor/) | tsl2561 0x29 | [all 4.14](https://github.com/beagleboard/linux/blob/4.14/drivers/iio/light/tsl2563.c) |
| [Time of flight sensor](http://wiki.seeedstudio.com/Grove-Time_of_Flight_Distance_Sensor-VL53L0X/) | vl53l0x 0x29 | [TBD](https://github.com/beagleboard/cloud9-examples/tree/master/PocketBeagle/Grove/VL53L0X) |
| [2x16 LCD with backlight](http://wiki.seeedstudio.com/Grove-LCD_RGB_Backlight/)  | hd44780 0x3e | [TBD](https://github.com/Seeed-Studio/grove-linux-driver/tree/master/src/hd44780) |
| [Temperature and humidity sensor](http://wiki.seeed.cc/Grove-TemptureAndHumidity_Sensor-High-Accuracy_AndMini-v1.0/) | th02 0x40 | [all 4.14](https://github.com/beagleboard/linux/blob/4.14/drivers/iio/humidity/si7005.c) |
| [ADC](http://wiki.seeedstudio.com/Grove-I2C_ADC/) | adc121c 0x50, adc121c 0x55 | [all 4.14](https://github.com/beagleboard/linux/blob/4.14/drivers/iio/adc/ti-adc081c.c) |
| [IMU 10DOF](http://wiki.seeedstudio.com/Grove-IMU_10DOF/) | mpu9250 0x68, bmp180 0x77 | TBD |
| [Barometer sensor (BME280)](http://wiki.seeedstudio.com/Grove-Barometer_Sensor-BME280/) | bme280 0x76 | TBD |

### [2x16 LCD with backlight](http://wiki.seeedstudio.com/Grove-LCD_RGB_Backlight/) extra details

Interface shows up at /dev/lcd0. See https://github.com/Seeed-Studio/grove-linux-driver/tree/master/src/hd44780. 

## UART4

### [GPS](http://wiki.seeed.cc/Grove-GPS/)

```sh
sudo apt install gpsd gpsd-clients
sudo gpsctl add /dev/ttyS4
gpsmon
```


# [mikroBus Grove Adapter](https://www.tindie.com/products/pmunts/mikrobus-grove-adapter-3/)

| Grove socket and pin | mikroBUS name | Position 1 PocketBeagle pin | Position 2 PocketBeagle pin |
| --- | --- | --- | --- |
| J1 - ANA - 1 | AIN | ```P1_2``` (AIN6/GPIO87) | ```P2_35``` (AIN5/GPIO86) |
| J1 - ANA - 2 | PWM | ```P2_1``` (PWM1A) | ```P1_36``` (PWM0A) |
| J2 - GPIO - 1 | RST | ```P1_4``` (GPIO89) | ```P2_33``` (GPIO45) |
| J2 - GPIO - 2 | INT | ```P2_3``` (GPIO23) | ```P1_34``` (GPIO26) |
| J3 - SER - 1 | RX | ```P2_5``` (UART4) | ```P1_32``` (UART0) |
| J3 - SER - 2 | TX | ```P2_7``` (UART4) | ```P1_30``` (UART0) |
| J4 - I2C - 1 | SCL | ```P2_9``` (I2C1) | ```P1_28``` (I2C2) |
| J4 - I2C - 2 | SDA | ```P2_11``` (I2C1) | ```P1_26``` (I2C2) |
