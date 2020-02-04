# BeagleBoard.org PocketBeagle Grove Kit

![](img/_DAS6325.jpg)

PocketBeagle is an ultra-tiny-yet-complete open-source USB-key-fob computer. PocketBeagle features an incredibly low cost, slick design, and simple usage, making PocketBeagle the ideal development board for beginners and professionals alike. Its rich features allow users to programmatically control external devices and obtain data from external devices.

Grove is a modular, standardized connector prototyping system. Consisting of Sensor, Actuator, Display, Communication, and Other function modules. Grove takes a building block approach to assemble electronics. Compared to the jumper or solder based system, it is easier to connect, experiment and build and simplifies the learning system. 

BeagleBoard.org PocketBeagle Grove Kit combines the Grove sensor modules with the powerful programming capabilities of PocketBeagle, allowing students to interact with music using real-world information such as light, touch, keyboard, Slide Potentiometer, posture and so on, to create cool projects.

## Hardware Overview

![](img/pin.jpg)


**Part List:**

- <font size="4" color="red">①</font> [Grove - Analog Microphone](TBD)
- <font size="4" color="red">②</font> [Grove - Chainable RGB LED](http://wiki.seeedstudio.com/Grove-Chainable_RGB_LED/)
- <font size="4" color="red">③</font> [Grove - Ultrasonic Distance Sensor](http://wiki.seeedstudio.com/Grove-Ultrasonic_Ranger/)
- <font size="4" color="red">④</font> [Grove - Rotary Angle Sensor](http://wiki.seeedstudio.com/Grove-Rotary_Angle_Sensor/)
- <font size="4" color="red">⑤</font> [Grove - Slide Potentiometer](http://wiki.seeedstudio.com/Grove-Slide_Potentiometer/)
- <font size="4" color="red">⑥</font> [Grove - Button](http://wiki.seeedstudio.com/Grove-Button/)
- <font size="4" color="red">⑦</font> [Grove - 12 Key Capacitive I2C Touch Sensor V2](http://wiki.seeedstudio.com/Grove-12_Key_Capacitive_I2C_Touch_Sensor_V2-MPR121/)
- <font size="4" color="red">⑧</font> [Grove - 3 Axis Digital Accelerometer](http://wiki.seeedstudio.com/Grove-3-Axis_Digital_Accelerometer-16g/)
- <font size="4" color="red">⑨</font> [Grove - Speaker Plus](http://wiki.seeedstudio.com/Grove-Speaker/)
- <font size="4" color="red">⑩</font> [Grove - 16x2 LCD](http://wiki.seeedstudio.com/Grove-16x2_LCD_Series/)
- <font size="4" color="red">⑪</font> [BeagleBoard.org PocketBeagle](https://beagleboard.org/pocket)
- <font size="4" color="red">⑫</font> [10pcs Alligator Cable](https://www.seeedstudio.com/10pcs-alligator-clip-test-lead-500mm-22awg-p-3087.html)
- <font size="4" color="red">⑬</font> SD+TF Card Reader
- <font size="4" color="red">⑭</font> WiFi Dongle
- <font size="4" color="red">⑮</font> Acrylic shell

## Setup the driver on pocketbeagle

firstly, you should visit [Getting_Started](https://github.com/beagleboard/pocketbeagle/wiki/System-Reference-Manual#331_Getting_Started) to get a start. the driver includes codec, wifi, and seeed-linux-overlays. we will describe it separately.
### connect wifi by using connmanctl

`connmanctl` is a tool that connects Pockbeagle to the internet with WiFi Dongle,please refer below command

```bash
robot@ev3dev:~$ sudo connmanctl
Error getting VPN connections: The name net.connman.vpn was not provided by any
connmanctl> enable wifi
Enabled wifi
connmanctl> scan wifi
Scan completed for wifi
connmanctl> services
*AO Wired                ethernet_b827ebbde13c_cable
                         wifi_e8de27077de3_hidden_managed_none
    AH04044914           wifi_e8de27077de3_41483034303434393134_managed_psk
    Frissie              wifi_e8de27077de3_46726973736965_managed_psk
    ruijgt gast          wifi_e8de27077de3_7275696a67742067617374_managed_psk
    schuur               wifi_e8de27077de3_736368757572_managed_psk
connmanctl> agent on
Agent registered
connmanctl> connect wifi_e8de27077de3_41      # You can use the TAB key at this point to autocomplete the name
connmanctl> connect wifi_e8de27077de3_41483034303434393134_managed_psk
Agent RequestInput wifi_e8de27077de3_41483034303434393134_managed_psk
  Passphrase = [ Type=psk, Requirement=mandatory ]
Passphrase? *************
Connected wifi_e8de27077de3_41483034303434393134_managed_psk
connmanctl> quit
```
we can use `ifconfig` to get IP of pocketbeagle

### Make and install the seeed-linux-dtverlays on pocketbeagle

- Step 1. update the Kernel.

```bash
sudo apt update
sudo apt-get install linux-headers-$(uname -r) -y
```

- Step 2. Get the `seeed-linux-dtoverlay` source code, install and reboot.(Default installed)

seeed-linux-dtoverlay is a packet that can make some Grove become a file that can be read and write on Linux.

```bash
cd ~
git clone https://github.com/Seeed-Studio/seeed-linux-dtverlays
cd ~/seeed-linux-dtverlays
make && sudo make install_bb
sudo echo uboot_overlay_addr0=/lib/firmware/PB-I2C1-TLV320AIC3104.dtbo >> /boot/uEnv.txt
sudo echo uboot_overlay_addr1=/lib/firmware/BB-GPIO-P9813.dtbo >> /boot/uEnv.txt
sudo echo uboot_overlay_addr2=/lib/firmware/BB-GPIO-HCSR04.dtbo >> /boot/uEnv.txt
sudo echo uboot_overlay_addr3=/lib/firmware/BB-GPIO-GROVE-BUTTON.dtbo >> /boot/uEnv.txt
sudo echo uboot_overlay_addr4=/lib/firmware/BB-I2C1-JHD1802.dtbo >> /boot/uEnv.txt
sudo echo uboot_overlay_addr5=/lib/firmware/BB-I2C2-ADXL34X.dtbo >> /boot/uEnv.txt
sudo echo uboot_overlay_addr6=/lib/firmware/BB-I2C2-MPR121.dtbo >> /boot/uEnv.txt
sudo reboot
```

!!!Note
        Please connect Grove with PocketBeagle with Grove shield firstly, then reboot.

- Step 3.Use `alsactl` command to configure TLV320AIC3104 codec

```bash
sudo alsactl restore 0 -f /etc/alsa/tlv320aic3104.state.txt
```

- Step 4.Check if the driver of codec install successfully

if the driver of codec installed successfully , you should view below information.

```bash
debian@beaglebone:~$ aplay -l
**** List of PLAYBACK Hardware Devices ****
card 0: Audio [GroveBaseCape Audio], device 0: davinci-mcasp.0-tlv320aic3x-hifi tlv320aic3x-hifi-0 [davinci-mcasp.0-tlv320aic3x-hifi tlv320aic3x-hifi-0]
  Subdevices: 1/1
  Subdevice #0: subdevice #0
```
