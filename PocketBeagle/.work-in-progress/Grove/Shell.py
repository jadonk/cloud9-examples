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
def main():
    print(GetCmdReturn('pwd'))
if __name__ == "__main__":
    main()
    