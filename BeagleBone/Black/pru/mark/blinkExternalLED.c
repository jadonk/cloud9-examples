#include <stdint.h>
#include <pru_cfg.h>
#include "resource_table_empty.h"
#include "prugpio.h"

#define	PRUN 1_1

volatile register unsigned int __R30;
volatile register unsigned int __R31;

void main(void) {
	int i;

	uint32_t *gpio6 = (uint32_t *)GPIO6;

	/* Clear SYSCFG[STANDBY_INIT] to enable OCP master port */
	CT_CFG.SYSCFG_bit.STANDBY_INIT = 0;

	for(i=0; i<100; i++) {
		gpio6[GPIO_SETDATAOUT]   = P9_25;	// Turn the USR1 LED on

		__delay_cycles(500000000/5);	 // Wait 1/2 second
		
		gpio6[GPIO_CLEARDATAOUT] = P9_25;	// Off

		__delay_cycles(500000000/5); 
		
	}
	__halt();
}

// Turns off triggers
#pragma DATA_SECTION(init_pins, ".init_pins")
#pragma RETAIN(init_pins)
const char init_pins[] =  
	"/sys/class/gpio/export\0 177\0" \
	"/sys/class/gpio/gpio177/direction\0out\0" \
	"\0\0";

