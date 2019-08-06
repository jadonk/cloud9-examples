////////////////////////////////////////
//	ring.pru0.c
//      Does the "Ring Test" given here: https://pub.pages.cba.mit.edu/ring/
//	Reads P1_33 and writes it to P1_36 as fast as it can.
//	Wiring:	P1_36 connects to the plus lead of an LED.  The negative lead of the
//			LED goes to a 220 Ohm resistor.  The other lead of the resistor goes
//			to ground (P2_21).
//              A Switch goes to P1_33 and 3.3V  (P1_14).
//	Setup:	config_pin P1_36 pruout and config_pin P1_33 to pruin
//	See:	prugpio.h to see which pins attach to R30
//	PRU:	pru0
////////////////////////////////////////
#include <stdint.h>
#include <pru_cfg.h>
#include <pru_ctrl.h>
#include <stddef.h>
#include <rsc_types.h>
#include "resource_table_empty.h"
#include "prugpio.h"

volatile register unsigned int __R30;
volatile register unsigned int __R31;

void main(void) {
	/* Read GPIO input P9_25 and invert to GPIO output P9_29 */
        while(1) {
		if(__R31 & P1_33)
			__R30 = 0;
		else
			__R30 = P1_36;
        }
}

#pragma DATA_SECTION(init_pins, ".init_pins")
#pragma RETAIN(init_pins)
const char init_pins[] =  
	"/sys/devices/platform/ocp/ocp:P1_36_pinmux/state\0pruout\0" \
	"/sys/devices/platform/ocp/ocp:P1_33_pinmux/state\0pruin\0" \
	"\0\0";
