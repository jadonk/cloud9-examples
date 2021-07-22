#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
import iio
import time
class ADC:
    """ADC of PocketBeagle"""
    def __init__(self):
        """Initialize the ADC of PocketBeagle using iio python library
        """    
        self.AIN = []
        #Scan the ADC of PocketBeagle by using IIO python library
        # self.contexts = iio.scan_contexts()
        self.ctx = iio.Context("local:")
        for dev in self.ctx.devices:
            if 'adc.0.auto' in dev.name:
                self.name = dev.name
        self.dev = self.ctx.find_device(self.name)
        if not self.dev:
            print("maybe you should reinstall the driver of ADC")
            return
        #Integrate all channels to self.AIN
        self.AIN.append(self.dev.find_channel("voltage0", False))
        self.AIN.append(self.dev.find_channel("voltage1", False))
        self.AIN.append(self.dev.find_channel("voltage2", False))
        self.AIN.append(self.dev.find_channel("voltage3", False))
        self.AIN.append(self.dev.find_channel("voltage4", False))
        self.AIN.append(self.dev.find_channel("voltage5", False))
        self.AIN.append(self.dev.find_channel("voltage6", False))
        self.AIN.append(self.dev.find_channel("voltage7", False))
    def get(self, n):
        """Get ADC's data
           n:The channel of ADC(0~7)
           return: data of ADC[n]
        """
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