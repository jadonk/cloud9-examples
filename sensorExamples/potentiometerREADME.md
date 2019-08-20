# Demo: Potentiometer

A specific voltage can be sent to the ADC1 channel using a potentiometer. 
Please keep in mind that each one of the ADC pins can only **handle 1.8V maximum**.

![alt text](potentiometer_bb.png "Potentiometer")

## Build and execute instructions
* Hook up a BeagleBone or BeagleBone Black to the breadboard as shown in the diagram.

Pin | Bone  | Pocket
--- | ----- | ------
1.8V | P9_32 | P1_18
GND  | P9_34 | P1_17
AIN1 | P9_40 | P1_21

* After clicking ‘run’, the ADC1 channel will output a reading between 0-1, 
where 0 is 0V and 1 is the maximum input voltage (1.8V).
* Adjust your potentiometer's knob and click run again. 
The lower the resistance, the higher voltage you will see.
* Alter the code to look at inputs on other analog input pins. 
A schematic showing all available ADC channels are listed 
[here](https://elinux.org/Beagleboard:Cape_Expansion_Headers#Cape_Expansion_Headers).
