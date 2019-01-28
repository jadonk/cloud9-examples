# Grove modules

This is a set of examples for using Seeed Grove modules with PocketBeagle, primarily using
the BeagleBoard.org PocketBeagle Grove Cape, but some other wiring options are examined as
well.

# BeagleBoard.org PocketBeagle Grove Cape

## I2C1/I2C2

### [Time of flight sensor](http://wiki.seeedstudio.com/Grove-Time_of_Flight_Distance_Sensor-VL53L0X/)

```sh
echo vl53l0x 0x29 | sudo tee /sys/bus/i2c/devices/i2c-2/new_device
cat /sys/bus/iio/devices/iio\:device1/in_distance_raw
```

# [mikroBus Grove Adapter](https://www.tindie.com/products/pmunts/mikrobus-grove-adapter-3/)

### ANA
* 
