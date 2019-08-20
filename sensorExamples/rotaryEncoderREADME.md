# Demo: Accurately Reading the Position of a Motor or Dial: Rotary Encoders

You have a motor or dial and want to detect rotation using a rotary encoder.

Use a rotary encoder (also called a _quadrature encoder_) connected to one of the Bone's eQEP ports, as shown below.

![alt text](rotaryEncoder_bb.png "Wiring a rotary encoder using eQEP2")

We are using a quadrature rotary encoder, which has two switches inside that open and close in such a manner that you can tell which way the shaft is turning. In this particular encoder, the two switches have a common lead, which is wired to ground. It also has a pushbutton switch wired to the other side of the device, which we aren't using. 

Wire the encoder to ```P8_11``` and ```P8_12```, as shown.

BeagleBone Black has built-in hardware for reading up to three encoders.  
Here, we use the _eQEP2_ encoder.

Try rotating the encoder clockwise and counter-clockwise. The values you get for ```speed``` and ```position``` will depend on which way you are turning the device and how quickly. You will need to press ^C (Ctrl-C) to end the program.