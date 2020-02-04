#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# [Grove - Button](http://wiki.seeedstudio.com/Grove-Button/) on UART4
# [Grove - Button](http://wiki.seeedstudio.com/Grove-Button/) on A5
import time
from Shell import GetCmdReturn,os
import evdev

class BUTTON:
    def __init__(self):
        try:
            p2_35_pinmux = open('/sys/devices/platform/ocp/ocp:P2_35_pinmux/state', 'w')
            print('gpio', file=p2_35_pinmux)
            p2_35_pinmux.close()
            p2_05_pinmux = open('/sys/devices/platform/ocp/ocp:P2_05_pinmux/state', 'w')
            print('gpio', file=p2_05_pinmux)
            p2_05_pinmux.close()
            if not os.path.exists('/proc/device-tree/gpio_keys/grove_button_1057_0@0'):
                GetCmdReturn('sudo mkdir -p \
                /sys/kernel/config/device-tree/overlays/BB-GPIO-GROVE-BUTTON')
                GetCmdReturn('sudo dd \
                of=/sys/kernel/config/device-tree/overlays/BB-GPIO-GROVE-BUTTON/dtbo \
                if=/lib/firmware/BB-GPIO-GROVE-BUTTON.dtbo')
                while not os.path.exists('/proc/device-tree/aliases/mpr121'):
                    time.sleep(0.1)   
            try:
                self.button = evdev.InputDevice("/dev/input/event1")
            except IOError as err:
                subprocess.call(['sudo', 'chmod', '777', '/dev/input/event1'])
                self.button = evdev.InputDevice("/dev/input/event1")
        except IOError as err:
            print("File Error:"+str(err))
            print("maybe you should reinstall the driver of button")
    def GetKeyStatus(self):  
        return self.button.active_keys()
    def read_loop(self):
        return self.button.read_loop()

def main():
    d = BUTTON()
    for event in d.read_loop():
        if event.type == evdev.ecodes.EV_KEY:
            print(d.GetKeyStatus())
            print(evdev.categorize(event))

if __name__ == "__main__":
    main()
