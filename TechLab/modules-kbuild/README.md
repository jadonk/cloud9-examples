# TechLab modules-kbuild

From https://github.com/e-ale/Code/tree/master/RESOURCES/modules-kbuild

## Setup (already done on workshop image)

```sh
sudo apt-get install linux-headers-`uname -r`
```

## Build and run

```sh
cd /var/lib/cloud9/TechLab/modules-kbuild
make
config-pin p1.33 gpio
sudo insmod red-module.ko 
lsmod
dmesg | tail
sudo rmmod red_module
dmesg | tail
```
