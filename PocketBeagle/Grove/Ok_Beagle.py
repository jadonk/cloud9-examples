# Copyright (c) 2020 SeeedStudio
# Author: Hansen Chen
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# [Grove - Analog Microphone](http://wiki.seeedstudio.com/Grove-Speaker/) on PWM
# [Grove - Grove - Speaker Plus](http://wiki.seeedstudio.com/Grove-Chainable_RGB_LED/) on UART2
# [Grove - Chainable RGB LED](http://wiki.seeedstudio.com/Grove-Chainable_RGB_LED/) on A2
import time
from RGBLed import P981X
import signal
from snowboy import snowboydecoder
from Shell import GetCmdReturn,os
interrupted = False

def signal_handler(signal, frame):
    global interrupted
    interrupted = True


def interrupt_callback():
    global interrupted
    return interrupted

# Check the Ok_Beagle.pmdl whether exist.
if not os.path.exists('/usr/lib/python3/dist-packages/snowboy/resources/models/Ok_Beagle.pmdl'):
    if os.path.exists('/var/lib/cloud9/PocketBeagle/Grove/Ok_Beagle.pmdl'): 
        GetCmdReturn('sudo mv /var/lib/cloud9/PocketBeagle/Grove/Ok_Beagle.pmdl \
        /usr/lib/python3/dist-packages/snowboy/resources/models/')
    else:
        print('Maybe you should Drag Ok_Beagle.pmdl to Could9')
        exit(1)
        

detector = snowboydecoder.HotwordDetector('/usr/lib/python3/dist-packages/snowboy/resources/models/Ok_Beagle.pmdl', sensitivity=0.5)

# capture SIGINT signal, e.g., Ctrl+C
signal.signal(signal.SIGINT, signal_handler)
print('Listening... Press Ctrl+C to exit')

def callback():
    """Make LED blink once
    """
    LED.set(0,255,255,0)
    LED.set(1,255,255,0)
    time.sleep(1)
    LED.set(0,0,0,0)
    LED.set(1,0,0,0)
    
LED = P981X()
LED.set(0,0,0,0)
LED.set(1,0,0,0)

# main loop
detector.start(detected_callback=callback,
               interrupt_check=interrupt_callback,
               sleep_time=0.03)

detector.terminate()
