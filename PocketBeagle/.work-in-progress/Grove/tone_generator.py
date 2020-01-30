#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import numpy as np
import pyaudio
import wave
import subprocess
from tqdm import tqdm

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

def Play_Music(file):
    # define stream chunk
    chunk = 1024
    # open a wav format music
    f = wave.open(file,"rb")
    # instantiate PyAudio
    p = pyaudio.PyAudio()
    # open stream
    stream = p.open(format = p.get_format_from_width(f.getsampwidth()),
                                channels = f.getnchannels(),
                                rate = f.getframerate(),
                                output = True)
    # read data
    data = f.readframes(chunk)

    # play stream
    datas = []
    while len(data) > 0:
        data = f.readframes(chunk)
        datas.append(data)
    for d in tqdm(datas):
        stream.write(d)
    # stop stream
    stream.stop_stream()
    stream.close()

    # close PyAudio
    p.terminate()

def synthesizer(freq,duration = 0.5,amp=250,sampling_freq=framerate):
    samples = amp * (np.sin(2*np.pi*np.arange(sampling_freq*duration)*freq/sampling_freq))
    samples = samples.astype(np.float16)
    return samples

def main():
    # sudo alsactl restore 0 -f /opt/source/bb.org-overlays/extras/tlv320aic3104.state.txt
    subprocess.call(['mkdir', '-p', '/tmp/scale'])
    tone_freq = [ v for v in sorted(tone_freq_map.values())]
    for i in range(len(tone_freq)):
        f = wave.open( "/tmp/scale/%s"%_SCALE_DEFS[i],"wb")
        f.setnchannels(channels)
        f.setsampwidth(sampwidth)
        f.setframerate(framerate)
        f.writeframes(synthesizer(tone_freq[i]).tostring())
        f.close()
        Play_Music("/tmp/scale/%s"%_SCALE_DEFS[i])

if __name__ == "__main__":
    main()