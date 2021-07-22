#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# Exploring iio library

import iio

ctx = iio.Context("local:") 

for dev in ctx.devices:
    print("%s %s" % (dev.id, dev.name))
