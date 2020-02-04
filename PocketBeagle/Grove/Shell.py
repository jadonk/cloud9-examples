#!/usr/bin/env python3
import os
def GetCmdReturn(cmd):
    r = os.popen(cmd)
    text = r.read() 
    r.close()
    return text.strip('\n')    
    
def main():
    print(GetCmdReturn('pwd'))
if __name__ == "__main__":
    main()