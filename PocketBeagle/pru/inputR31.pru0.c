////////////////////////////////////////
//	blinkR30.pru0.c
//	Reads input in P1_33 via the R31 register and blinks the USR3 LED
//	Wiring:	A switch between P1_33 and 3.3V (P1_14)
//	Setup:	config_pin P1_33 pruin
//	See:	prugpio.h to see which pins attach to R31
//	PRU:	pru0
////////////////////////////////////////
#include <stdint.h>
#include <pru_cfg.h>
#include "resource_table_empty.h"
#include "prugpio.h"

volatile register unsigned int __R30;
volatile register unsigned int __R31;

void main(void) {
	uint32_t *gpio1 = (uint32_t *)GPIO1;

	/* Clear SYSCFG[STANDBY_INIT] to enable OCP master port */
	CT_CFG.SYSCFG_bit.STANDBY_INIT = 0;

	while(1) {
		if(__R31 & P1_33) {
            gpio1[GPIO_SETDATAOUT]   = USR3;      // Turn on LED
        } else
            gpio1[GPIO_CLEARDATAOUT] = USR3;      // Turn off LED
	}
	__halt();
}

// Turns off triggers and sets pinmux
#pragma DATA_SECTION(init_pins, ".init_pins")
#pragma RETAIN(init_pins)
const char init_pins[] =  
	"/sys/class/leds/beaglebone:green:usr3/trigger\0none\0" \
	"/sys/devices/platform/ocp/ocp:P1_33_pinmux/state\0pruin\0" \
	"\0\0";
