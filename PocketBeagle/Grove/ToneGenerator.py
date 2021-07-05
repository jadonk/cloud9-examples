#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
import numpy as np
import pyaudio
import wave
import time
from Shell import GetCmdReturn
import os
import sys

tone_freq_map={"do": 261.5, "re": 293.4,"me": 329.5,"fa": 349.1,"so": 391.7, \
"la": 440,"ti": 493.8,"do+":523}
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
def synthesizer(freq,duration=2,amp=32000,sampling_freq=framerate):
    """produce the tone list 
        freq:frequency of tone
        duration: duration of tone
        amp：Gain of tone
        sampling_freq : sampling frequency of tone
    """
    alpha = 4
    tt = np.arange(sampling_freq*duration)/sampling_freq
    samples = amp * np.sin(2*np.pi*freq*tt) * np.exp(-alpha*tt)
    samples = samples.astype(np.int16)
    return samples

def rebuildScale():
     # Rebuild the /tmp/scale
    GetCmdReturn('sudo rm -rf /tmp/scale')
    while os.path.exists('/tmp/scale'):
        time.sleep(0.1)    
    GetCmdReturn('sudo mkdir /tmp/scale')
    while not os.path.exists('/tmp/scale'):
        time.sleep(0.1)
    GetCmdReturn('sudo chown debian:debian /tmp/scale')
   
def generateScale():
    tone_freq = [ v for v in sorted(tone_freq_map.values())]
    for i in range(len(tone_freq)):
        # Set tone to wav
        if not os.path.exists("/tmp/scale/%s"%_SCALE_DEFS[i]):
            # print("/tmp/scale/%s not found"%_SCALE_DEFS[i])
            f = wave.open( "/tmp/scale/%s"%_SCALE_DEFS[i],"wb")
            f.setnchannels(channels)
            f.setsampwidth(sampwidth)
            f.setframerate(framerate)
            f.writeframes(synthesizer(tone_freq[i]).tostring())
            f.close()
            print("/tmp/scale/%s generated successfully"%_SCALE_DEFS[i])

def main():
    if not os.path.exists("/tmp/scale/"):
        rebuildScale()
    generateScale()

if __name__ == "__main__":
    main()
