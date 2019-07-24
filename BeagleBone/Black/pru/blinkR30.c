////////////////////////////////////////
//	blinkR30.c
//	Blinks LEDs wired to P9_29 (and others) by writing register R30 on the PRU
//	Wiring:	P9_29 connects to the plus lead of an LED.  The negative lead of the
//			LED goes to a 220 Ohm resistor.  The other lead of the resistor goes
//			to ground.
//	Setup:	config_pin P9_29 pruout
//	See:	prugpio.h to see which pins attach to R30
//	PRU:	pru0
////////////////////////////////////////
#include <stdint.h>
#include <pru_cfg.h>
#include "resource_table_empty.h"
#include "prugpio.h"

// Tells which PRU to run on.  Must run on pru1_1 for the P8 and P9 pins used here.
#define	PRUN 0

volatile register unsigned int __R30;
volatile register unsigned int __R31;

void main(void) {
	int i;

	// Select which pins to toggle.  These are all on pru1_1
	uint32_t gpio = P9_29;

	/* Clear SYSCFG[STANDBY_INIT] to enable OCP master port */
	CT_CFG.SYSCFG_bit.STANDBY_INIT = 0;

	for(i=0; i<10; i++) {
		__R30 |= gpio;					// Set the GPIO pin to 1
		__delay_cycles(500000000/5);    // Wait 1/2 second
		__R30 &= ~gpio;					// Clear the GPIO pin
		__delay_cycles(500000000/5); 
		}
	__halt();
}

// No need to turn off triggers or set pin direction
