#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
import iio
import time
import sys
import subprocess
import os

class ADC:
    def __init__(self):
        self.AIN = []
        self.contexts = iio.scan_contexts()
        self.ctx = iio.Context("local:")
        self.dev = self.ctx.find_device("44e0d000.tscadc:adc.0.auto")
        if not self.dev:
            print("maybe you should reinstall the driver of ADC")
            return
        self.AIN.append(self.dev.find_channel("voltage0", False))
        self.AIN.append(self.dev.find_channel("voltage1", False))
        self.AIN.append(self.dev.find_channel("voltage2", False))
        self.AIN.append(self.dev.find_channel("voltage3", False))
        self.AIN.append(self.dev.find_channel("voltage4", False))
        self.AIN.append(self.dev.find_channel("voltage5", False))
        self.AIN.append(self.dev.find_channel("voltage6", False))
        self.AIN.append(self.dev.find_channel("voltage7", False))

    def get(self, n):
        return int(self.AIN[n].attrs["raw"].value)

def main():
    AIN = ADC()
    while True:
        for i in range(8):
            x = AIN.get(i)
            print('%04d  ' % (x), end='')
        print('\r', end='')
        time.sleep(0.1)

if __name__ == "__main__":
    main()