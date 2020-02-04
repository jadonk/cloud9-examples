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