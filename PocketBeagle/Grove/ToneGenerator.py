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

import numpy as np
import pyaudio
import wave
import time
from Shell import GetCmdReturn,os

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

def synthesizer(freq,duration = 10,amp=250,sampling_freq=framerate):
    """produce the tone list 
        freq:frequency of tone
        duration: duration of tone
        amp：Gain of tone
        sampling_freq : sampling frequency of tone
    """
    samples = amp * (np.sin(2*np.pi*np.arange(sampling_freq*duration)*freq/sampling_freq))
    samples = samples.astype(np.float16)
    return samples

def main():
    # Rebuild the /tmp/scale
    GetCmdReturn('sudo rm -rf /tmp/scale')
    if not os.path.exists('/tmp/scale'):
        GetCmdReturn('sudo mkdir /tmp/scale')
        while not os.path.exists('/tmp/scale'):
            time.sleep(0.1)
        GetCmdReturn('sudo touch do.wav')
    tone_freq = [ v for v in sorted(tone_freq_map.values())]
    
    for i in range(len(tone_freq)):
        # Set tone to wav
        TONE_NAME = _SCALE_DEFS[i]
        GetCmdReturn('sudo chmod 777 /tmp/scale/$TONE_NAME')
        f = wave.open( "/tmp/scale/%s"%_SCALE_DEFS[i],"wb")
        f.setnchannels(channels)
        f.setsampwidth(sampwidth)
        f.setframerate(framerate)
        f.writeframes(synthesizer(tone_freq[i]).tostring())
        f.close()
        print("/tmp/scale/%s generated successfully"%_SCALE_DEFS[i])
if __name__ == "__main__":
    main()