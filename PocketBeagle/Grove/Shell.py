#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
import os
import time
def GetCmdReturn(cmd):
    """Run CMD using os.popen and get the CMD's output.
        cmd : The shell cmd 
        return :the CMD's output
    """
    r = os.popen(cmd)
    text = r.read() 
    r.close()
    return text.strip('\n')    
def InstallDTBO(DTBO):
    """Install Dtbo using dd cmd
        DTBO :  name of DTBO 
    """
    # Build file using mkdir
    GetCmdReturn('sudo mkdir -p \
    /sys/kernel/config/device-tree/overlays/$DTBO')  
    # Install dtbo using dd
    DTBO_PATH = DTBO + '.dtbo'
    GetCmdReturn('sudo dd \
    of=/sys/kernel/config/device-tree/overlays/$DTBO/dtbo \
    if=/lib/firmware/$DTBO_PATH')   
def ConfigGPIO(PinName):
    """config pin function to GPIO
        PinName : Name of pin 
    """
    PinName = PinName + '_pinmux'
    PinName = open('/sys/devices/platform/ocp/ocp:%s/state'%PinName, 'w')
    print('gpio', file=PinName)
    PinName.close()
def InstallModule(Module):    
    """Install Module  
        Module : Name of Module 
    """    
    GetCmdReturn('sudo modprobe -s %s'%Module)
    Module = Module.replace('-','_')
    while not Module in GetCmdReturn('lsmod | grep %s'%Module):
        time.sleep(0.1)  
def RemoveModule(Module):    
    """Install Module  
        Module : Name of Module 
    """    
    Module = Module.replace('-','_')
    GetCmdReturn('sudo rmmod -s %s || true '%Module)
    while Module in GetCmdReturn('lsmod | grep %s'%Module):
        time.sleep(0.1)       
def ReinstallModule(Module):
    """Reinstall Module using InstallModule and RemoveModule  
        Module : Name of Module 
    """
    RemoveModule(Module)
    InstallModule(Module)
def main():
    print(GetCmdReturn('pwd'))
    ConfigGPIO('P1_31')
    ReinstallModule('adxl345_i2c')
if __name__ == "__main__":
    main()