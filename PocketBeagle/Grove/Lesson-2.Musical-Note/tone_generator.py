#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import numpy as np
import pyaudio
import wave
import os
import time
import subprocess
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
framerate = 192000

def synthesizer(freq,duration = 10,amp=250,sampling_freq=framerate):
    samples = amp * (np.sin(2*np.pi*np.arange(sampling_freq*duration)*freq/sampling_freq))
    samples = samples.astype(np.float16)
    return samples

def main():
    if not os.path.exists('/home/debian/scale'):
        os.popen('mkdir /home/debian/scale')
        while not os.path.exists('/home/debian/scale'):
            time.sleep(0.1)
    tone_freq = [ v for v in sorted(tone_freq_map.values())]
    for i in range(len(tone_freq)):
        # subprocess.call(['sudo', 'chmod'  , '777', "/home/debian/scale/%s"%_SCALE_DEFS[i]])
        f = wave.open( "/home/debian/scale/%s"%_SCALE_DEFS[i],"wb")
        f.setnchannels(channels)
        f.setsampwidth(sampwidth)
        f.setframerate(framerate)
        f.writeframes(synthesizer(tone_freq[i]).tostring())
        f.close()
        print("/home/debian/scale/%s generated successfully"%_SCALE_DEFS[i])
if __name__ == "__main__":
    main()