#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# [Grove - Button](http://wiki.seeedstudio.com/Grove-Button/) on UART4
# [Grove - Button](http://wiki.seeedstudio.com/Grove-Button/) on A5
import time
from Shell import InstallDTBO,ConfigGPIO,GetCmdReturn
import os
import evdev
class BUTTON:
    def __init__(self):
        """Initialize the BUTTON using evdev python library"""
        self.Path = '/proc/device-tree/gpio_keys/grove_button_1057_0@0'
        try:
            # Config p2_35 and p2_05 to GPIO mode
            ConfigGPIO('P2_35')
            ConfigGPIO('P2_05')
            # Check BB-GPIO-GROVE-BUTTON whether install successfully
            # if not reinstall it            
            if not os.path.exists(self.Path):
                InstallDTBO('BB-GPIO-GROVE-BUTTON')
                while not os.path.exists(self.Path):
                    time.sleep(0.1)   
            #Input Button using evdev python library
            try:
                self.button = evdev.InputDevice("/dev/input/event1")
            except IOError as err:
                GetCmdReturn('sudo chmod 777 /dev/input/event1')
                self.button = evdev.InputDevice("/dev/input/event1")
        except IOError as err:
            print("File Error:"+str(err))
            print("maybe you should reinstall the driver of button")
    def GetKeyStatus(self):  
        """Get two button's Value
            return:[](Button isn't pressed),[256],[257](Button is pressed)
        """
        return self.button.active_keys()
    def read_loop(self):
        """Read two button's status constantly
            return:two button's status
        """
        return self.button.read_loop()
def main():
    d = BUTTON()
    for event in d.read_loop():
        if event.type == evdev.ecodes.EV_KEY:
            print(d.GetKeyStatus())
            print(evdev.categorize(event))
if __name__ == "__main__":
    main()