# TechLab modules-kbuild

From https://github.com/e-ale/Code/tree/master/RESOURCES/modules-kbuild

```sh
make
config-pin p1.33 gpio
sudo insmod red-module.ko 
lsmod
dmesg | tail
sudo rmmod red_module 
```
