# Grove Music Kit for Pocket Beagle


![](https://github.com/SeeedDocument/Grove-Music-Kit-for-Pocket-Beagle/raw/master/img/_DAS6325.jpg)



PocketBeagle is an ultra-tiny-yet-complete open-source USB-key-fob computer. PocketBeagle features an incredibly low cost, slick design, and simple usage, making PocketBeagle the ideal development board for beginners and professionals alike. Its rich features allow users to programmatically control external devices and obtain data from external devices.

Grove is a modular, standardized connector prototyping system. Consisting of Sensor, Actuator, Display, Communication, and Other function modules. Grove takes a building block approach to assemble electronics. Compared to the jumper or solder based system, it is easier to connect, experiment and build and simplifies the learning system. 

The Grove Music Kit for Pocket Beagle combines the Grove sensor modules with the powerful programming capabilities of Pocket Beagle, allowing students to interact with music using real-world information such as light, touch, keyboard, Slide Potentiometer, posture and so on, to create cool projects.




## Haedware Overview

![](https://github.com/SeeedDocument/Grove-Music-Kit-for-Pocket-Beagle/raw/master/img/pin.jpg)



**Part List:**

- <font size="4" color="red">①</font> [Grove - Sound Sensor](http://wiki.seeedstudio.com/Grove-Sound_Sensor/)
- <font size="4" color="red">②</font> [Grove - Chainable RGB LED](http://wiki.seeedstudio.com/Grove-Chainable_RGB_LED/)
- <font size="4" color="red">③</font> [Grove - Ultrasonic Distance Sensor](http://wiki.seeedstudio.com/Grove-Ultrasonic_Ranger/)
- <font size="4" color="red">④</font> [Grove - Rotary Angle Sensor](http://wiki.seeedstudio.com/Grove-Rotary_Angle_Sensor/)
- <font size="4" color="red">⑤</font> [Grove - Slide Potentiometer](http://wiki.seeedstudio.com/Grove-Slide_Potentiometer/)
- <font size="4" color="red">⑥</font> [Grove – Button](http://wiki.seeedstudio.com/Grove-Button/)
- <font size="4" color="red">⑦</font> [Grove - 12 Key Capacitive I2C Touch Sensor V2](http://wiki.seeedstudio.com/Grove-12_Key_Capacitive_I2C_Touch_Sensor_V2-MPR121/)
- <font size="4" color="red">⑧</font> [Grove - 3 Axis Digital Accelerometer](http://wiki.seeedstudio.com/Grove-3-Axis_Digital_Accelerometer-16g/)
- <font size="4" color="red">⑨</font> [Grove – Speaker](http://wiki.seeedstudio.com/Grove-Speaker/)
- <font size="4" color="red">⑩</font> [Grove – 16x2 LCD](http://wiki.seeedstudio.com/Grove-16x2_LCD_Series/)
- <font size="4" color="red">⑪</font> [Pocket Beagle with Grove shield](https://www.seeedstudio.com/PocketBeagle-OSD3358ARM-Cortex-A8-512MB-RAM-p-2888.html)
- <font size="4" color="red">⑫</font> [10pcs Alligator Cable](https://www.seeedstudio.com/10pcs-alligator-clip-test-lead-500mm-22awg-p-3087.html)
- <font size="4" color="red">⑬</font> SD+TF Card Reader
- <font size="4" color="red">⑭</font> WiFi Dongle
- <font size="4" color="red">⑮</font> Acrylic shell

## Setup the driver on pocketbeagle

### Setup the codec on pocketbeagle

Although pocket beagle has not a codec, we use the TLV320AIC3104 codec to play music.And you should refer below introduce to install it.

- Step 1. Get the `TLV320AIC3104` codec source code, install and reboot.

```bash
git clone -b beagle-master https://github.com/turmary/bb.org-overlays.git
cd ~/bb.org-overlays
make && sudo make install
```

Use `echo` to add `PB-I2C1-TLV320AIC3104.dtbo` to /boot/uEnv.txt then reboot. 

```bash
sudo echo uboot_overlay_addr0=/lib/firmware/PB-I2C1-TLV320AIC3104.dtbo >> /boot/uEnv.txt 
sudo reboot
```

- Step 2.Use `aplay -l` to check if the codec is successfully installed

```bash
aplay -l
```

If the following information is displayed, the installation was successful

```bash
debian@beaglebone:~$ aplay -l
**** List of PLAYBACK Hardware Devices ****
card 0: Audio [GroveBaseCape Audio], device 0: davinci-mcasp.0-tlv320aic3x-hifi tlv320aic3x-hifi-0 [davinci-mcasp.0-tlv320aic3x-hifi tlv320aic3x-hifi-0]
  Subdevices: 1/1
  Subdevice #0: subdevice #0
```

- Step 3.Use `wget` command to get configure file and config TLV320AIC3104 codec with alsactl

```bash
wget https://github.com/beagleboard/bb.org-overlays/files/3877583/tlv320aic3104.state.txt 
mv tlv320aic3104.state.txt  tlv320aic3104.state
sudo alsactl restore 0 -f tlv320aic3104.state
```

### Make and install the seeed-linux-dtverlays on pocketbeagle

seeed-linux-dtoverlay is a packet that can make some Grove become a file that can be read and write on Linux.

```bash
git clone https://github.com/Seeed-Studio/seeed-linux-dtverlays
cd ~/seeed-linux-dtverlays
make 
sudo make install_bb
```

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


## Lesson – 1. Control the Light

### Description:

In this lesson, students will light up the RGB LED, and learn how to use sound and rotary angle to change the light of RGB LED.

### Hardware Requirement:

- [Grove - Sound Sensor](http://wiki.seeedstudio.com/Grove-Sound_Sensor/)
- [Grove - Rotary Angle Sensor](http://wiki.seeedstudio.com/Grove-Rotary_Angle_Sensor/)
- [Grove - Chainable RGB LED](http://wiki.seeedstudio.com/Grove-Chainable_RGB_LED/)


### Hardware Connection
 
- Plug the Grove - Sound Sensor into **A0** port
- Plug the Grove - Rotary Angle Sensor into **A5** port
- Grove - Chainable RGB LED into **A2** port
- Power the Pocket Beagle via the **micro USB** port


![](https://github.com/SeeedDocument/Grove-Music-Kit-for-Pocket-Beagle/raw/master/img/_DAS6312.jpg)



### Software

- Step 1.Use `echo ` to add `BB-GPIO-P9813.dtbo` to /boot/uEnv.txt then reboot. 

```bash
sudo echo uboot_overlay_addr1=/lib/firmware/BB-GPIO-P9813.dtbo >> /boot/uEnv.txt
sudo reboot
```
!!!Note
        Please connect Grove with Pocket Beagle with Grove shield firstly, then reboot.
- Step 2.make and install driver of rgb led

```bash
cd ~/seeed-linux-dtverlays/modules/p9813
make && sudo make install
```
- Step 3. Build Control_the_Light.py by using `nano` and please follow below code.
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
    with open('/sys/bus/iio/devices/iio:device0/%s'%_AIN_DEFS[AIN], 'r') as f:
        text = f.readlines()
        text[0] = text[0].strip('\n')
        return text[0]
def InitRGBLed(leds):    
    with open('/dev/p981x0', 'w') as f:
        f.write('N %d\n'%leds)   
def setColorRGB(led, red, green, blue):
    with open('/dev/p981x0', 'w') as f:
        f.write('D %d %d %d %d\n'%(led,red,green,blue))    
def main():
    InitRGBLed(1)
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
        setColorRGB(0,Rotary_Angle_Data,Sound_Data,0)
        time.sleep(0.1)
if __name__ == "__main__":
    main()
```
- Step 4. run Control_the_Light.py

```bash
   sudo python3 Control_the_Light.py
```

!!!success
        Now please turn the rotary angle sensor slowly, and see how the RGB LED changes its light.


-------------

## Lesson – 2. Musical Note

### Description:

In this lesson, students can move their hand in front of the ultrasonic distance sensor, the LCD will show the distance of the hand, and speaker will play different musical note based on different distance.

### Hardware Requirement:

- [Grove - Ultrasonic Distance Sensor](http://wiki.seeedstudio.com/Grove-Ultrasonic_Ranger/)
- [Grove – 16x2 LCD](http://wiki.seeedstudio.com/Grove-16x2_LCD_Series/)
- [Grove – Speaker](http://wiki.seeedstudio.com/Grove-Speaker/)


### Hardware Connection
 
- Plug the Grove - Ultrasonic Distance Sensor into **A2** port
- Plug the Grove – 16x2 LCD into **I2C1** port
- Plug the Grove – Speaker into **UART2** port
- Power the Pocket Beagle via the **micro USB** port

![](https://github.com/SeeedDocument/Grove-Music-Kit-for-Pocket-Beagle/raw/master/img/project2.jpg)


### Software

- Step 1.Remove `uboot_overlay_addr1=/lib/firmware/BB-GPIO-P9813.dtbo` in /boot/uEnv.txt and Use `echo ` to add `BB-GPIO-HCSR04.dtbo`,`BB-I2C1-JHD1802` to /boot/uEnv.txt then reboot. 

```bash
# sudo apt install linux-image-4.19.79-ti-r30 linux-headers-4.19.79-ti-r30
sudo echo uboot_overlay_addr1=/lib/firmware/BB-GPIO-HCSR04.dtbo >> /boot/uEnv.txt 
sudo echo uboot_overlay_addr2=/lib/firmware/BB-I2C1-JHD1802.dtbo >> /boot/uEnv.txt 
sudo reboot
```

!!!Note
        Please connect Grove with Pocket Beagle with Grove shield firstly, then reboot.

- Step 2.make then install driver of 16x2 LCD and driver of Ultrasonic Distance Sensor. 

```bash
cd ~/seeed-linux-dtverlays/modules/hd44780
make && sudo make install
sudo modprobe hd44780
cd ~/seeed-linux-dtverlays/modules/hcsr04
make && sudo make install
```

- Step 3.install pyaudio and tqdm

```bash
sudo apt install portaudio19-dev python-all-dev python3-all-dev -y
wget http://portaudio.com/archives/pa_stable_v190600_20161030.tgz
tar   zxvf pa_stable_v190600_20161030.tgz
cd ~/portaudio
.configure
make && sudo make install 
sudo pip3 install pyaudio 
sudo pip3 install tqdm
```

- Step 4. New scale file and genarate tone by using below python code 

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

tone_freq_map={"do": 261.5, "re": 293.4,"me": 329.5,"fa": 349.1,"so": 391.7,"la": 440,"ti": 493.8}
_SCALE_DEFS = [
   'do.wav',
   're.wav',
   'me.wav',
   'fa.wav',
   'so.wav',
   'la.wav',
   'ti.wav'
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

    # paly stream
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


- Step 5. Build Musical_Note.py by using `nano` and please follow below code.

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
    with open('/dev/lcd0', 'w') as f:
        f.write('\x1b[2J')
        f.write('\x1b[H')
    with open('/dev/lcd0', 'w') as f:
        f.write('%s'%text)
    time.sleep(.5)
def get_distance(): 
    with open('/sys/bus/iio/devices/iio:device1/in_distance_input', 'r') as f:
        text = f.readlines()
        text[0] = text[0].strip('\n')
        return text[0]
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

    # paly stream
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
        # int_value = int(distance)
        print(distance)
        if int(distance) < 70 :
            Play_Music("/home/debian/scale/%s"%_SCALE_DEFS[int(int(distance)/10)])
        time.sleep(.5)
if __name__ == "__main__":
    main()
```
- Step 6. run Musical_Note.py

```bash
   sudo python3 Musical_Note.py
```

!!!success
        Now please please slowly change the distance between your hand and the ultrasonic distance sensor, you can find the distance value in the LCD change and the music switched by the distance.




--------


## Lesson – 3. Switch the Music

### Description:

In this lesson, students will learn how to use the 2 buttons to select the next song or the last song. The LCD will show the name of the song.

### Hardware Requirement:

- [Grove – Button x 2](http://wiki.seeedstudio.com/Grove-Button/)
- [Grove – Speaker](http://wiki.seeedstudio.com/Grove-Speaker/)
- [Grove – 16x2 LCD](http://wiki.seeedstudio.com/Grove-16x2_LCD_Series/)


### Hardware Connection
 
- Plug the Grove – Button into **A0** and **A2** port
- Plug the Grove – 16x2 LCD into **I2C1** port
- Plug the Grove – Speaker into **UART2** port
- Power the Pocket Beagle via the **micro USB** port


![](https://github.com/SeeedDocument/Grove-Music-Kit-for-Pocket-Beagle/raw/master/img/project-3.jpg)


### Software

- Step 1.Remove `uboot_overlay_addr1=/lib/firmware/BB-GPIO-HCSR04.dtbo` in /boot/uEnv.txt and Use `echo ` to add `BB-GPIO-GROVE-BUTTON.dtbo`,`BB-I2C1-JHD1802` to /boot/uEnv.txt then reboot. 

```bash
# sudo apt install linux-image-4.19.79-ti-r30 linux-headers-4.19.79-ti-r30
sudo echo uboot_overlay_addr3=/lib/firmware/BB-GPIO-GROVE-BUTTON.dtbo >> /boot/uEnv.txt 
sudo echo uboot_overlay_addr2=/lib/firmware/BB-I2C1-JHD1802.dtbo >> /boot/uEnv.txt 
sudo reboot
```

!!!Note
        Please connect Grove with Pocket Beagle with Grove shield firstly, then reboot.

- Step 2.install driver of 16x2 LCD and config pin of button. 

```bash
sudo modprobe hd44780
config-pin P1_31 gpio
```

- Step 3.install evdev

```bash
sudo pip3 install evdev
```

- Step 4. Build Switch_the_Music.py by using `nano` and please follow below code.

```bash
nano Switch_the_Music.py
```

```python
#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
import time,threading
from evdev import InputDevice
import wave
import os
import pyaudio
def Get_Key_Status():  
    key = InputDevice("/dev/input/event1")
    # print(key.active_keys())
    return key.active_keys()
def setText(text):
    with open('/dev/lcd0', 'w') as f:
        f.write('\x1b[2J')
        f.write('\x1b[H')
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
    setText("Hello World")
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
if __name__ == "__main__":
    main()
```
- Step 6. run Musical_Note.py

```bash
   sudo python3 Switch_the_Music.py
```


!!!success
        Now please try to press the two buttons, check the LCD, and listen to the music.



-----

## Lesson – 4. Download Music via the WIFI dongle

### Description:
In this lesson, students will learn how to download mp3 files from the Internet via the WIFI dongle, and they can also practice the skill learn from Lesson3 to switch the music.

### Hardware Requirement:

- [Grove – Button x 2](http://wiki.seeedstudio.com/Grove-Button/)
- [Grove – Speaker](http://wiki.seeedstudio.com/Grove-Speaker/)
- [Grove – 16x2 LCD](http://wiki.seeedstudio.com/Grove-16x2_LCD_Series/)
- USB WIFI dongle


### Hardware Connection
 
- Plug the Grove – Button into **A2** and **A0** port
- Plug the Grove – 16x2 LCD into **I2C** port
- Plug the Grove – Speaker into **A5** port
- Plug the WiFi dongle into the **USB** Port
- Power the Pocket Beagle via the **micro USB** port


![](https://github.com/SeeedDocument/Grove-Music-Kit-for-Pocket-Beagle/raw/master/img/project-4.jpg)


### Software

- Step 1.Connect wifi that connects with your computer by using `connmanctl`

if you don't know how to use `connmanctl`, maybe you should review the previous lessons

- Step 2.Download [winscp](https://winscp.net/eng/download.php).

- Step 3. Open winscp and type the hostname and username 

[](https://github.com/SeeedDocument/Grove-Music-Kit-for-Pocket-Beagle/raw/master/img/drag_music_file.png)

the hostname is an IP address of Pockbeagle that can use ifconfig to find it. The username is `debian`

- Step 4. Drag your music file to `/home/debian/scale`

[](https://github.com/SeeedDocument/Grove-Music-Kit-for-Pocket-Beagle/raw/master/img/winscp.png)

- Step 5. run Musical_Note.py

```bash
   sudo python3 Switch_the_Music.py
```

!!!success
        Default music is boring and bad taste? Now, with the help of WiFi, you can download the music meet your own flavor.

----


## Lesson – 5. KeyBoard Player

### Description:

In this lesson, students will learn how to use the capacitive touch sensor to play different musical note.

### Hardware Requirement:

- [Grove - 12 Key Capacitive I2C Touch Sensor V2](http://wiki.seeedstudio.com/Grove-12_Key_Capacitive_I2C_Touch_Sensor_V2-MPR121/)
- [Grove – Speaker](http://wiki.seeedstudio.com/Grove-Speaker/)


### Hardware Connection
 
- Plug the Grove – Speaker into **A5** port
- Plug the Grove - 12 Key Capacitive I2C Touch Sensor V2 into **I2C** port
- Power the Pocket Beagle via the **micro USB** port


![](https://github.com/SeeedDocument/Grove-Music-Kit-for-Pocket-Beagle/raw/master/img/project-5.jpg)


### Software

```
to be continue ... ...
```


!!!success
        Try to touch the Capacitive key, image it as a keyboard, and play your music.


----


## Lesson – 6. Start the Party


### Description:

In this lesson, students will learn how to use the capacitive touch sensor to play the song <Twinkle Star>. And the RGB LED will have different color based on different music note.

### Hardware Requirement:

- [Grove - 12 Key Capacitive I2C Touch Sensor V2](http://wiki.seeedstudio.com/Grove-12_Key_Capacitive_I2C_Touch_Sensor_V2-MPR121/)
- [Grove – Speaker](http://wiki.seeedstudio.com/Grove-Speaker/)
- [Grove - Slide Potentiometer](http://wiki.seeedstudio.com/Grove-Slide_Potentiometer/)
- [Grove - Chainable RGB LED](http://wiki.seeedstudio.com/Grove-Chainable_RGB_LED/)



### Hardware Connection
 
- Plug the Grove – Speaker into **A5** port
- Plug the Grove - 12 Key Capacitive I2C Touch Sensor V2 into **I2C** port
- Plug the Grove - Slide Potentiometer into **A2** port
- Plug the Chainable RGB LED into **PWM** port
- Power the Pocket Beagle via the **micro USB** port


![](https://github.com/SeeedDocument/Grove-Music-Kit-for-Pocket-Beagle/raw/master/img/project-6.jpg)


### Software

```
to be continue ... ...
```


!!!success
        Just control the music as lesson 5, and you can see the color of RGB LED change.



----


## Lesson – 7. Music Box

### Description:

In this lesson, students will learn how to use the Grove – 3-Axis Accelerometer to control RGB LED and Speaker. At last, he can make a smart box, by putting different side of the box on the table, the box will have different color and play different music.


### Hardware Requirement:

- [Grove - 3 Axis Digital Accelerometer](http://wiki.seeedstudio.com/Grove-3-Axis_Digital_Accelerometer-16g/)
- [Grove – Speaker](http://wiki.seeedstudio.com/Grove-Speaker/)
- [Grove - Chainable RGB LED](http://wiki.seeedstudio.com/Grove-Chainable_RGB_LED/)


### Hardware Connection

- Plug the Grove – Speaker into **A5** port
- Plug the Grove - 3 Axis Digital Accelerometer into **A2** port
- Plug the Chainable RGB LED into **PWM** port
- Power the Pocket Beagle via the **micro USB** port

![](https://github.com/SeeedDocument/Grove-Music-Kit-for-Pocket-Beagle/raw/master/img/project-7.jpg)


### Software

```
to be continue ... ...
```


!!!success
        Here you go, a smart music box. Just rotate the music box and dance with different music.

----