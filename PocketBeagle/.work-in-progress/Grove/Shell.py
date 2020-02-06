#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
import os
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
        DTBO :  DTBO package to be installed
        return :the CMD's output
    """
    # Build file using mkdir
    GetCmdReturn('sudo mkdir -p \
    /sys/kernel/config/device-tree/overlays/$DTBO')  
    # Install dtbo using dd
    DTBO_PATH = DTBO + '.dtbo'
    GetCmdReturn('sudo dd \
    of=/sys/kernel/config/device-tree/overlays/$DTBO/dtbo \
    if=/lib/firmware/$DTBO_PATH')   
    
def main():
    print(GetCmdReturn('pwd'))
    InstallDTBO('BB-GPIO-GROVE-BUTTON')
if __name__ == "__main__":
    main()