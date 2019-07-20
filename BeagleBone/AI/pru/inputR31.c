// Reads input in P8_13 via the R31 register and blinks the USR3 LED
// Wire a switch between P8_13 and ground

#include <stdint.h>
#include <pru_cfg.h>
#include "resource_table_empty.h"
#include "prugpio.h"

// Tells which PRU to run on.  Must run on pru1_1 for the P8 and P9 pins used here.
#define	PRUN 1_1

volatile register unsigned int __R30;
volatile register unsigned int __R31;

void main(void) {
	uint32_t *gpio3 = (uint32_t *)GPIO3;

	/* Clear SYSCFG[STANDBY_INIT] to enable OCP master port */
	CT_CFG.SYSCFG_bit.STANDBY_INIT = 0;

	while(1) {
		if(__R31&P8_13) {
            gpio3[GPIO_SETDATAOUT]   = USR3;      // Turn off LED
        } else
            gpio3[GPIO_CLEARDATAOUT] = USR3;      // Turn on LED
	}
	__halt();
}

// Turns off triggers
#pragma DATA_SECTION(init_pins, ".init_pins")
#pragma RETAIN(init_pins)
const char init_pins[] =  
	"/sys/class/leds/beaglebone:green:usr3/trigger\0none\0" \
	"\0\0";
