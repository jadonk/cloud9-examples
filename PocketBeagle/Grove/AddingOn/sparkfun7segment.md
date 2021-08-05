# Adding a SparkFun 7-segment Display

[SparkFun 7-Segment Serial Display](https://www.sparkfun.com/products/11441) 
combines a classic 4-digit 7-segment display 
and a microcontroller allowing you to control every segment individually
using [these i2c commands](https://github.com/sparkfun/Serial7SegmentDisplay/wiki/Special-Commands). 
It can be easily added to the Grove Kit using a JST-4 to female lead connected to
either of the Grove i2c ports.  Here I'm using i2c2.


Once wired, run `i2cdetect` to see the sensor.
The `2` at the end of the command says to look at bus `2`.

```
bone$ i2cdetect -y -r 2
     0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f
00:          -- -- -- -- -- -- -- -- -- -- -- -- -- 
10: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
20: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
30: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
40: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
50: -- -- -- -- -- -- -- 57 -- -- -- -- -- -- -- -- 
60: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
70: -- 71 -- -- -- -- -- --     
 ```
 
 Here we see it appearing at its default address `0x71`. You can clear the
 display by sending `0x76`
 ```
 bone$ i2cset -y 2 0x71 0x76
```
The following will display the characters `0123`
```
bone$ i2cset -y 2 0x71 0
bone$ i2cset -y 2 0x71 1
bone$ i2cset -y 2 0x71 2
bone$ i2cset -y 2 0x71 3
```

See the python file for examples of how to control the decimals, fade the display
and control the individual segments.