#include <stdint.h>
#include <pru_cfg.h>
#include "resource_table_empty.h"
#include "prugpio.h"

// Tells which PRU to run on.  Must run on pru1_1 for the P8 and P9 pins used here.
#define	PRUN 1_1

volatile register unsigned int __R30;
volatile register unsigned int __R31;

void main(void) {
	int i;
	uint32_t *gpio3 = (uint32_t *)GPIO3;

	// Select which pins to toggle.  These are all on pru1_1
	uint32_t gpio = P9_14 | P9_16 | P8_15 | P8_16 | P8_26;

	/* Clear SYSCFG[STANDBY_INIT] to enable OCP master port */
	CT_CFG.SYSCFG_bit.STANDBY_INIT = 0;

	for(i=0; i<100; i++) {
		__R30 |= gpio;		// Set the GPIO pin to 1

		__delay_cycles(500000000/5);    // Wait 1/2 second

		__R30 &= ~gpio;		// Clearn the GPIO pin

		__delay_cycles(500000000/5); 
			}
	__halt();
}

// No need to turn off triggers or set pin direction
