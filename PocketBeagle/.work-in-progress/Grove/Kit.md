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

### Make and install the seeed-linux-dtverlays on pocketbeagle

- Step 1. update the Kernel.

```bash
sudo apt update
sudo apt install linux-image-4.19.79-ti-r30 linux-headers-4.19.79-ti-r30 -y
```

- Step 2. Get the `seeed-linux-dtoverlay` source code, install and reboot.

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
sudo alsactl restore 0 -f /opt/source/bb.org-overlays/extras/tlv320aic3104.state.txt
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

## Lesson - 1. Control the Light

### Description:

In this lesson, students will light up the RGB LED, and learn how to use sound and rotary angle to change the light of RGB LED.

### Hardware Requirement:

- [Grove - Analog Microphone](http://wiki.seeedstudio.com/Grove-Sound_Sensor/)
- [Grove - Rotary Angle Sensor](http://wiki.seeedstudio.com/Grove-Rotary_Angle_Sensor/)
- [Grove - Chainable RGB LED](http://wiki.seeedstudio.com/Grove-Chainable_RGB_LED/)


### Hardware Connection
 
- Plug the Grove - Analog Microphone into **A0** port
- Plug the Grove - Rotary Angle Sensor into **A5** port
- Grove - Chainable RGB LED into **A2** port
- Power PocketBeagle via the **micro USB** port


![](img/_DAS6312.jpg)



### Software

- Step 1. Install driver of Chainable RGB LED and Check it weather install successfully

```bash
cd ~/seeed-linux-dtverlays/modules/p9813
make && sudo make install
sudo modprobe p9813
```

if the driver of Chainable RGB LED installed successfully , you should view below information.

```bash 
debian@beaglebone:~$ lsmod | grep p9813
p9813                  16384  0
debian@beaglebone:~$ ls /dev/p981x0
p981x0
```

- Step 2. Build Control_the_Light.py by using `nano` and please follow below code.

```
nano Control_the_Light.py
```

```python
#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
import time,sys
AIN0 = 0
AIN1 = 1
AIN2 = 2
AIN3 = 3
AIN4 = 4
AIN5 = 5
AIN6 = 6
AIN7 = 7
_AIN_DEFS = [
   'in_voltage0_raw',
   'in_voltage1_raw',
   'in_voltage2_raw',
   'in_voltage3_raw',
   'in_voltage4_raw',
   'in_voltage5_raw',
   'in_voltage6_raw',
   'in_voltage7_raw'
   ]
def GetAdcData(AIN):
    try:
        with open('/sys/bus/iio/devices/iio:device0/%s'%_AIN_DEFS[AIN], 'r') as f:
            text = f.readlines()
            text[0] = text[0].strip('\n')
            return text[0]
    except IOError as err:
        print("File Error:"+str(err))
        print("maybe you should reinstall the driver of ADC")
def InitRGBLed(leds):
    try:
        with open('/dev/p981x0', 'w') as f:
            f.write('N %d\n'%leds)
    except IOError as err:
        print("File Error:"+str(err))
        print("maybe you should reinstall the driver of p981x")
def setColorRGB(led, red, green, blue):
    try:
        with open('/dev/p981x0', 'w') as f:
            f.write('D %d %d %d %d\n'%(led,red,green,blue))
    except IOError as err:
        print("File Error:"+str(err))
        print("maybe you should reinstall the driver of p981x")
def main():
    InitRGBLed(2)
    while True:

        Sound_Data = GetAdcData(AIN0)
        Rotary_Angle_Data = GetAdcData(AIN5)
        Sound_Data = int(int(Sound_Data)/1800*255)
        Rotary_Angle_Data = int(int(Rotary_Angle_Data)/3300*255)
        if Rotary_Angle_Data > 255 : 
            Rotary_Angle_Data = 255
        if Sound_Data > 255 :
            Sound_Data = 255
        print("Sound_Data is %d"%Sound_Data)
        print("Rotary_Angle_Data is %d"%Rotary_Angle_Data)
        setColorRGB(0,Rotary_Angle_Data,0,0)
        setColorRGB(1,0,Sound_Data,0)
        time.sleep(0.1)
if __name__ == "__main__":
    main()
```

- Step 3. run Control_the_Light.py,and you can use `Ctrl+\` to quit this process

```bash
   sudo python3 Control_the_Light.py
```

!!!success
        Now please turn the rotary angle sensor slowly, and see how the RGB LED changes its light.


-------------

## Lesson - 2. Musical Note

### Description:

In this lesson, students can move their hand in front of the ultrasonic distance sensor, the LCD will show the distance of the hand, and speaker will play different musical note based on different distance.

### Hardware Requirement:

- [Grove - Ultrasonic Distance Sensor](http://wiki.seeedstudio.com/Grove-Ultrasonic_Ranger/)
- [Grove - 16x2 LCD](http://wiki.seeedstudio.com/Grove-16x2_LCD_Series/)
- [Grove - Speaker Plus](http://wiki.seeedstudio.com/Grove-Speaker/)


### Hardware Connection
 
- Plug the Grove - Ultrasonic Distance Sensor into **A0** port
- Plug the Grove - 16x2 LCD into **I2C1** port
- Plug the Grove - Speaker Plus into **UART2** port
- Power PocketBeagle via the **micro USB** port

![](img/project2.jpg)


### Software

- Step 1.make then install driver of 16x2 LCD and driver of Ultrasonic Distance Sensor.

```bash
cd ~/seeed-linux-dtverlays/modules/hd44780
make && sudo make install
sudo modprobe hd44780
cd ~/seeed-linux-dtverlays/modules/hcsr04
make && sudo make install
sudo modprobe hcsr04
sudo config-pin P1_31 gpio
```

if the driver of 16x2 LCD and Ultrasonic Distance Sensor installed successfully , you should view below information.

```bash
debian@beaglebone:~$ lsmod | grep hcsr04
hcsr04                 16384  0
debian@beaglebone:~$ cat /sys/bus/iio/devices/iio:device1/name
hcsr04_1057@20
debian@beaglebone:~$ lsmod | grep hd44780
hd44780                16384  0
debian@beaglebone:~$ ls /dev/lcd0
/dev/lcd0
```

!!!Note
        Please connect Grove with Pocket Beagle with Grove shield firstly, then reboot.

- Step 2.install pyaudio and tqdm

```bash
cd ~
sudo apt install portaudio19-dev python-all-dev python3-all-dev -y
sudo pip3 install pyaudio
sudo pip3 install tqdm
```

- Step 3. New scale file and genarate tone by using below python code

```bash
mkdir ~/scale
nano tone_generator.py
```

```python
#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import numpy as np
import pyaudio
import wave
from tqdm import tqdm

tone_freq_map={"do": 261.5, "re": 293.4,"me": 329.5,"fa": 349.1,"so": 391.7,"la": 440,"ti": 493.8,"do+":523}
_SCALE_DEFS = [
   'do.wav',
   're.wav',
   'me.wav',
   'fa.wav',
   'so.wav',
   'la.wav',
   'ti.wav',
   'do+.wav'
   ]
channels = 1
sampwidth = 2
framerate = 44100

def Play_Music(file):
    # define stream chunk
    chunk = 1024
    # open a wav format music
    f = wave.open(file,"rb")
    # instantiate PyAudio
    p = pyaudio.PyAudio()
    # open stream
    stream = p.open(format = p.get_format_from_width(f.getsampwidth()),
                                channels = f.getnchannels(),
                                rate = f.getframerate(),
                                output = True)
    # read data
    data = f.readframes(chunk)

    # play stream
    datas = []
    while len(data) > 0:
        data = f.readframes(chunk)
        datas.append(data)
    for d in tqdm(datas):
        stream.write(d)
    # stop stream
    stream.stop_stream()
    stream.close()

    # close PyAudio
    p.terminate()

def synthesizer(freq,duration = 0.5,amp=250,sampling_freq=framerate):
    samples = amp * (np.sin(2*np.pi*np.arange(sampling_freq*duration)*freq/sampling_freq))
    samples = samples.astype(np.float16)
    return samples

def main():
    tone_freq = [ v for v in sorted(tone_freq_map.values())]
    for i in range(len(tone_freq)):
        f = wave.open( "/home/debian/scale/%s"%_SCALE_DEFS[i],"wb")
        f.setnchannels(channels)
        f.setsampwidth(sampwidth)
        f.setframerate(framerate)
        f.writeframes(synthesizer(tone_freq[i]).tostring())
        f.close()
        Play_Music("/home/debian/scale/%s"%_SCALE_DEFS[i])

if __name__ == "__main__":
    main()
```

```bash
sudo python3 tone_generator.py
```

- Step 4. Build Musical_Note.py by using `nano` and please follow below code.

```bash
nano Musical_Note.py
```

```python
#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
import time,sys
import pyaudio
import wave
from tqdm import tqdm
_SCALE_DEFS = [
   'do.wav',
   're.wav',
   'me.wav',
   'fa.wav',
   'so.wav',
   'la.wav',
   'ti.wav'
   ]
def setText(text):
    try:
        with open('/dev/lcd0', 'w') as f:
            f.write('\x1b[2J')
            f.write('\x1b[H')
    except IOError as err:
        print("File Error:"+str(err))
        print("maybe you should reinstall the driver of hd44780")
    with open('/dev/lcd0', 'w') as f:
        f.write('%s'%text)
    time.sleep(.5)
def get_distance():
    try:
        with open('/sys/bus/iio/devices/iio:device1/in_distance_input', 'r') as f:
            text = f.readlines()
            text[0] = text[0].strip('\n')
            return text[0]
    except IOError as err:
        print("File Error:"+str(err))
        print("maybe you should reinstall the driver of hcsr04")
def Play_Music(file):
    # define stream chunk
    chunk = 1024
    # open a wav format music
    f = wave.open(file,"rb")
    # instantiate PyAudio
    p = pyaudio.PyAudio()
    # open stream
    stream = p.open(format = p.get_format_from_width(f.getsampwidth()),
                                channels = f.getnchannels(),
                                rate = f.getframerate(),
                                output = True)
    # read data
    data = f.readframes(chunk)

    # play stream
    datas = []
    while len(data) > 0:
        data = f.readframes(chunk)
        datas.append(data)
    for d in tqdm(datas):
        stream.write(d)
    # stop stream
    stream.stop_stream()
    stream.close()

    # close PyAudio
    p.terminate()
def main():
    while True:
        distance = get_distance()
        setText("The Distance: \r\n{} cm".format(distance))
        print(distance)
        if int(distance) < 70 :
            Play_Music("/home/debian/scale/%s"%_SCALE_DEFS[int(int(distance)/10)])
        time.sleep(.5)
if __name__ == "__main__":
    main()
```

- Step 5. run Musical_Note.py,and you can use `Ctrl+\` to quit this process

```bash
   sudo python3 Musical_Note.py
```

!!!success
        Now please please slowly change the distance between your hand and the ultrasonic distance sensor, you can find the distance value in the LCD change and the music switched by the distance.

## Lesson - 3. Switch the Music

### Description:

In this lesson, students will learn how to use the 2 buttons to select the next song or the last song. the buttons not only can select the next song or the last song by press instantly but also can play music by Press longly.

The LCD will show the name of the song.

### Hardware Requirement:

- [Grove - Button x 2](http://wiki.seeedstudio.com/Grove-Button/)
- [Grove - Speaker Plus](http://wiki.seeedstudio.com/Grove-Speaker/)
- [Grove - 16x2 LCD](http://wiki.seeedstudio.com/Grove-16x2_LCD_Series/)

### Hardware Connection
 
- Plug the Grove - Button into **A5** and **UART4** port
- Plug the Grove - 16x2 LCD into **I2C1** port
- Plug the Grove - Speaker Plus into **UART2** port
- Power PocketBeagle via the **micro USB** port

![](img/project-3.jpg)

### Software

- Step 1.install driver of 16x2 LCD and config pin of Button.

```bash
sudo modprobe hd44780
sudo config-pin P2_35 gpio
sudo config-pin P2_05 gpio
cd ~
```

if the driver of 16x2 LCD installed successfully , you should view below information.

```bash
debian@beaglebone:~$ lsmod | grep hd44780
hd44780                16384  0
debian@beaglebone:~$ ls /dev/lcd0
/dev/lcd0
```

- Step 2.Install evdev

```bash
sudo pip3 install evdev
```

- Step 3. Build Switch_the_Music.py by using `nano` and please follow below code.

```bash
nano Switch_the_Music.py
```

```python
#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
import time
from evdev import InputDevice
import wave
import os
import pyaudio
def Get_Key_Status():  
    try:
        key = InputDevice("/dev/input/event1")
    except IOError as err:
        print("File Error:"+str(err))
        print("maybe you should reinstall the driver of button")
    # print(key.active_keys())
    return key.active_keys()
def setText(text):
    try:
        with open('/dev/lcd0', 'w') as f:
            f.write('\x1b[2J')
            f.write('\x1b[H')
    except IOError as err:
        print("File Error:"+str(err))
        print("maybe you should reinstall the driver of hd44780")
    with open('/dev/lcd0', 'w') as f:
        f.write('%s'%text)
def Play_Music(file):
    # define stream chunk 
    chunk = 1024
    # open a wav format music
    f = wave.open(file,"rb")
    # instantiate PyAudio
    p = pyaudio.PyAudio()
    key = InputDevice("/dev/input/event1")
    def callback(in_data, frame_count, time_info, status):
        data = f.readframes(frame_count)
        if len(key.active_keys()):
            return (data,pyaudio.paContinue)
        return (data,pyaudio.paComplete)
    # open stream
    stream = p.open(format = p.get_format_from_width(f.getsampwidth()),
                                channels = f.getnchannels(),
                                rate = f.getframerate(),
                                output = True,
                                stream_callback=callback)
    # read data
    stream.start_stream()
    while stream.is_active():
        time.sleep(0.01)  
    # stop stream
    stream.stop_stream()
    stream.close()
    # close PyAudio
    p.terminate()

def main():
    MusciIndex = 0
#    setText("Hello World")
    files= os.listdir("/home/debian/scale")
    print(files)
    while True:
        KeyStatus = Get_Key_Status()
        if(len(KeyStatus)):
            if KeyStatus[0] == 256:
                MusciIndex = MusciIndex + 1
                if MusciIndex > 6:
                    MusciIndex = 0
                Play_Music("/home/debian/scale/%s"%files[MusciIndex])
            if KeyStatus[0] == 257:
                MusciIndex = MusciIndex - 1
                if MusciIndex < 0:
                    MusciIndex = 6
                Play_Music("/home/debian/scale/%s"%files[MusciIndex])
            setText("scale: \r\n{}".format(files[MusciIndex]))
        time.sleep(0.05)
if __name__ == "__main__":
    main()
```

- Step 4. run Musical_Note.py,and you can use `Ctrl+\` to quit this process

```bash
   sudo python3 Switch_the_Music.py
```

!!!success
        Now please try to press the two buttons, check the LCD, and listen to the music.

## Lesson - 4. Download Music via the WIFI dongle

### Description:

In this lesson, students will learn how to download mp3 files from the Internet via the WIFI dongle, and they can also practice the skill learn from Lesson3 to switch the music.

### Hardware Requirement:

- [Grove - Button x 2](http://wiki.seeedstudio.com/Grove-Button/)
- [Grove - Speaker Plus](http://wiki.seeedstudio.com/Grove-Speaker/)
- [Grove - 16x2 LCD](http://wiki.seeedstudio.com/Grove-16x2_LCD_Series/)
- USB WIFI dongle


### Hardware Connection

- Plug the Grove - Button into **A5** and **UART4** port
- Plug the Grove - 16x2 LCD into **I2C1** port
- Plug the Grove - Speaker Plus into **UART2** port
- Plug the WiFi dongle into the **USB** Port
- Power PocketBeagle via the **micro USB** port


![](img/project-4.jpg)


### Software

- Step 1.Connect wifi that connects with your computer by using `connmanctl`

if you don't know how to use `connmanctl`, maybe you should review the previous lessons

- Step 2.Use `wget` to get test.wav

```bash
cd ~/home/debian/scale
wget http://www.wavsource.com/snds_2018-06-03_5106726768923853/people/comedians/carlin_letter.wav
```

!!!Note
        Please select *.wav to /home/debian/scale 

- Step 3. run Switch_the_Music.py,and you can use `Ctrl+\` to quit this process

```bash
   sudo python3 Switch_the_Music.py
```

!!!success
        Default music is boring and bad taste? Now, with the help of WiFi, you can download the music meet your own flavor.

## Lesson - 5. KeyBoard Player

### Description:

In this lesson, students will learn how to use the capacitive touch sensor to play different musical note.

### Hardware Requirement:

- [Grove - 12 Key Capacitive I2C Touch Sensor V2](http://wiki.seeedstudio.com/Grove-12_Key_Capacitive_I2C_Touch_Sensor_V2-MPR121/)
- [Grove - Speaker Plus](http://wiki.seeedstudio.com/Grove-Speaker/)

### Hardware Connection

- Plug the Grove - Speaker Plus into **UART2** port
- Plug the Grove - 12 Key Capacitive I2C Touch Sensor V2 into **I2C2** port
- Power PocketBeagle via the **micro USB** port

![](img/project-5.jpg)

### Software

- Step 1. install driver of 12 Key Capacitive I2C Touch Sensor V2

```bash
cd ~/seeed-linux-dtverlays/modules/mpr121
make && sudo make install
sudo modprobe mpr121
cd ~
```

if the driver of 12 Key Capacitive I2C Touch Sensor V2 installed successfully , you should view below information.

```bash
debian@beaglebone:~$ lsmod | grep mpr121
mpr121                 16384  0
debian@beaglebone:~$ cat /sys/devices/platform/ocp/4819c000.i2c/i2c-2/2-005b/name
mpr121
```
if you cannot view information described above. maybe you can check if item connect correct and reboot.

!!!Note
        Please connect Grove to PocketBeagle with PocketBeagle Grove Cape firstly, then reboot.

- Step 2. Build KeyBoard_Player.py by using `nano` and please follow below code.

```python
#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
import time
import wave
import os
import pyaudio
from tqdm import tqdm
CHANNEL_NUM                               = 12
ResultStr = [1, 1, 1]
_SCALE_DEFS = [
   'do.wav',
   're.wav',
   'me.wav',
   'fa.wav',
   'so.wav',
   'la.wav',
   'ti.wav',
   'do+.wav'
   ]
def Play_Music(file):
    # define stream chunk
    chunk = 1024
    # open a wav format music
    f = wave.open(file,"rb")
    # instantiate PyAudio
    p = pyaudio.PyAudio()
    # open stream
    stream = p.open(format = p.get_format_from_width(f.getsampwidth()),
                                channels = f.getnchannels(),
                                rate = f.getframerate(),
                                output = True)
    # read data
    data = f.readframes(chunk)

    # play stream
    datas = []
    while len(data) > 0:
        data = f.readframes(chunk)
        datas.append(data)
    for d in tqdm(datas):
        stream.write(d)
    # stop stream
    stream.stop_stream()
    stream.close()

    # close PyAudio
    p.terminate()
def parse_and_print_result(result):
    touch_flag = [0]*CHANNEL_NUM
    if result != 0:
        result = result % 1000
        ResultStr[0] = result // 100
        ResultStr[1] = result % 100 // 10
        ResultStr[2] = result % 100 % 10
        result = ResultStr[0] * (1<<8) | ResultStr[1] * (1<<4) | ResultStr[2]
        for i in range(CHANNEL_NUM):
            if(result & 1 << i):
                if(0 == touch_flag[i]):
                    touch_flag[i] = 1
                    print("Channel %d is pressed"%i)
            else:
                if(1 == touch_flag[i]):
                    touch_flag[i] = 0
                    print("Channel %d is released"%i)
    return touch_flag
def GetMpr121Data():
    try:
        with open('/sys/devices/platform/ocp/4819c000.i2c/i2c-2/2-005b/mpr121_data', 'r') as f:
            text = f.readlines()
            text[0] = text[0].strip('\n')
            return text[0]
    except IOError as err:
        print("File Error:"+str(err))
        print("maybe you should reinstall the driver of mpr121")
def main():
    while True:
        try:
           GetMpr121 = int(GetMpr121Data())
        except ValueError as err:
            print("Multi-touch is not supported")
        Mpr121Data = parse_and_print_result(GetMpr121)
        if any(Mpr121Data) != False:
            for i in range(CHANNEL_NUM):
                if(Mpr121Data[i] == 1):
                    if i > 3 :
                        Play_Music("/home/debian/scale/%s"%_SCALE_DEFS[i-4])
                    else :
                        Play_Music("/home/debian/scale/%s"%_SCALE_DEFS[i])
        time.sleep(0.05)
if __name__ == "__main__":
    main()
```

- Step 3. Run KeyBoard_Player.py,and you can use `Ctrl+\` to quit this process

```bash
sudo python3 KeyBoard_Player.py
```

!!!success
        Try to touch the Capacitive key, image it as a keyboard, and play your music.


## Lesson - 6. Start the Party


### Description:

In this lesson, students will learn how to use the capacitive touch sensor to play the song <Twinkle Star>. And the RGB LED will have different color based on different music note.

### Hardware Requirement:

- [Grove - 12 Key Capacitive I2C Touch Sensor V2](http://wiki.seeedstudio.com/Grove-12_Key_Capacitive_I2C_Touch_Sensor_V2-MPR121/)
- [Grove - Speaker Plus](http://wiki.seeedstudio.com/Grove-Speaker/)
- [Grove - Chainable RGB LED X 2](http://wiki.seeedstudio.com/Grove-Chainable_RGB_LED/)



### Hardware Connection
 
- Plug the Grove - Speaker Plus into **UART2** port
- Plug the Grove - 12 Key Capacitive I2C Touch Sensor V2 into **I2C2** port
- Plug the Grove - Chainable RGB LED X 2 into **A2** port
- Power PocketBeagle via the **micro USB** port


![](img/project-6.jpg)


### Software

- Step 1. install driver of I2C Touch Sensor V2 and RGB LED

```bash
cd ~/seeed-linux-dtverlays/modules/mpr121
make && sudo make install
sudo modprobe mpr121
cd ~/seeed-linux-dtverlays/modules/p9813
make && sudo make install
sudo modprobe p9813
cd ~
```


!!!success
        Just control the music as lesson 5, and you can see the color of RGB LED change.



----


## Lesson - 7. Music Box

### Description:

In this lesson, students will learn how to use the Grove - 3-Axis Accelerometer to control RGB LED and Speaker. At last, he can make a smart box, by putting different side of the box on the table, the box will have different color and play different music.


### Hardware Requirement:

- [Grove - 3 Axis Digital Accelerometer](http://wiki.seeedstudio.com/Grove-3-Axis_Digital_Accelerometer-16g/)
- [Grove - Speaker](http://wiki.seeedstudio.com/Grove-Speaker/)
- [Grove - Chainable RGB LED](http://wiki.seeedstudio.com/Grove-Chainable_RGB_LED/)


### Hardware Connection

- Plug the Grove - Speaker into **A5** port
- Plug the Grove - 3 Axis Digital Accelerometer into **A2** port
- Plug the Chainable RGB LED into **PWM** port
- Power PocketBeagle via the **micro USB** port

![](img/project-7.jpg)


### Software

```
to be continue ... ...
```


!!!success
        Here you go, a smart music box. Just rotate the music box and dance with different music.

## Lesson - 8. Hello Kitt-AI

In this lesson, students will learn how to install the snowboy of Kitt-AI and use it.

### Hardware Requirement:

- [Grove - Speaker Plus](http://wiki.seeedstudio.com/Grove-Speaker/)
- [Grove - Analog Microphone](http://wiki.seeedstudio.com/Grove-Chainable_RGB_LED/)

### Hardware Connection

- Plug the Grove - Speaker Plus into **UART2** port
- Plug the Grove - Analog Microphone into **PWM** port
- Power the Pocket Beagle via the **micro USB** port
are
![](https://github.com/hansonCc/Grove-Music-Kit-for-Pocket-Beagle/raw/master/img/project-7.jpg)

### Software

- Step 1. Check the sound card. if  the sound card install successfully, you should view below information

```bash
debian@beaglebone:~$ aplay -l
**** List of PLAYBACK Hardware Devices ****
card 0: Audio [GroveBaseCape Audio], device 0: davinci-mcasp.0-tlv320aic3x-hifi tlv320aic3x-hifi-0 [davinci-mcasp.0-tlv320aic3x-hifi tlv320aic3x-hifi-0]
  Subdevices: 1/1
  Subdevice #0: subdevice #0
debian@beaglebone:~$ arecord -l
**** List of CAPTURE Hardware Devices ****
card 0: Audio [GroveBaseCape Audio], device 0: davinci-mcasp.0-tlv320aic3x-hifi tlv320aic3x-hifi-0 [davinci-mcasp.0-tlv320aic3x-hifi tlv320aic3x-hifi-0]
  Subdevices: 1/1
  Subdevice #0: subdevice #0
```

- Step 2.Use apt-get install sox, portaudio

```bash
sudo apt-get install python-pyaudio python3-pyaudio sox -y
```

!!!Note

    if you should the sound of the record is small, maybe you can use  `amixer cset numid=33,iface=MIXER,name='PGA Capture Volume' 80%` to enlarge PGA Capture Volume.


- Step 3.Use apt-get install libpcre3, swig

```bash
cd ~
sudo apt-get install libpcre3 libpcre3-dev swig -y
```

- Step 4.Install the atlas matrix computing library

```bash
sudo apt-get install libatlas-base-dev -y
```

- Step 5.Get snowboy from github and compile a Python Wrapper

```bash
cd ~
git clone https://github.com/Kitt-AI/snowboy.git
cd ~/snowboy/swig/Python3
make
```

SWIG will generate a `_snowboydetect.so` file and a simple (but hard-to-read) python wrapper `snowboydetect.py`. We have provided a higher level python wrapper `snowboydecoder.py` on top of that.

- Step 6.Modify the snowboydecoder.py

First, you can use bash below to found snowboydecoder.py

```bash
cd ~/snowboy/examples/Python3/
```

snowboydecoder.py have a problem, you can fix it by Modifying the `import` of line 5 of snowboydecoder.py.we can make this effect by using code below.

```python
#from . import snowboydetect
import snowboydetect
```
And we need to change the code from line 164 to line 180 of snowboydecoder.py to adapt our mic.

```python
        def audio_callback(in_data, frame_count, time_info, status):
            data_array = np.fromstring(in_data, dtype='int16')
            channel0 = data_array[0::2]
            in_data = channel0.tostring()
            self.ring_buffer.extend(in_data)
            play_data = chr(0) * len(in_data)
            return play_data, pyaudio.paContinue

        with no_alsa_error():
            self.audio = pyaudio.PyAudio()
        self.stream_in = self.audio.open(
            input=True, output=False,
            format=pyaudio.paInt16,
            channels=2,
            rate=16000,
            frames_per_buffer=2048,
            stream_callback=audio_callback)
```

Finally, you should modify the sensitivity of snowboy by editing line 27 of demo.py

```python
    detector = snowboydecoder.HotwordDetector(model, sensitivity=0.8)    
```

- Step 7.Run the demo

```python
cd ~/snowboy/examples/Python3/
sudo python3 demo.py ~/snowboy/resources/models/snowboy.umdl
```

!!!success

        When we speak `snowboy` to the mic, and the speaker will make a 'ding' tone.

- Step 8.more information about  snowboy of Kitt-AI

we only provide very easy demo about snowboy of Kitt-AI.you can visit [snowboy](https://github.com/Kitt-AI/snowboy) to view the more information.

if you want to use other hotword. we also provide an easy way for you.

**1** Create your personal hotword model through our [website](https://snowboy.kitt.ai/)

**2** Put your personal model in snowboy/resources/models

**3** Run the demo


```python
cd ~/snowboy/examples/Python3/
sudo python3 demo.py ~/snowboy/resources/models/***.pmdl
```

if you want to control the led with snowboy, and you can visit [BlinkWithSonwboy](http://docs.kitt.ai/snowboy/#control-an-led-with-python) to learn it.
