////////////////////////////////////////
//	blinkR30.c
//	Reads input in P9_25 via the R31 register and blinks the USR3 LED
//	Wiring:	A switch between P9_25 and 3.3V (P9_3 or P9_4)
//	Setup:	config_pin P9_25 pruin
//	See:	prugpio.h to see which pins attach to R30
//	PRU:	pru0
////////////////////////////////////////
// 
// Wire 

#include <stdint.h>
#include <pru_cfg.h>
#include "resource_table_empty.h"
#include "prugpio.h"

// Tells which PRU to run on.  Must run on pru1_1 for the P8 and P9 pins used here.
#define	PRUN 0

volatile register unsigned int __R30;
volatile register unsigned int __R31;

void main(void) {
	uint32_t *gpio1 = (uint32_t *)GPIO1;

	/* Clear SYSCFG[STANDBY_INIT] to enable OCP master port */
	CT_CFG.SYSCFG_bit.STANDBY_INIT = 0;

	while(1) {
		if(__R31 & P9_25) {
            gpio1[GPIO_SETDATAOUT]   = USR3;      // Turn on LED
        } else
            gpio1[GPIO_CLEARDATAOUT] = USR3;      // Turn off LED
	}
	__halt();
}

// Turns off triggers
#pragma DATA_SECTION(init_pins, ".init_pins")
#pragma RETAIN(init_pins)
const char init_pins[] =  
	"/sys/class/leds/beaglebone:green:usr3/trigger\0none\0" \
	"\0\0";
