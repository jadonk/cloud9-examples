// Control a ws2812 (NeoPixel) display, All on or all off
#include <stdint.h>
#include <pru_cfg.h>
#include "resource_table_empty.h"
#include "init_pins_empty.h"
#include "prugpio.h"

#define PRUN 1_1

#define STR_LEN 40
#define	oneCyclesOn		700/5	// Stay on 700ns
#define oneCyclesOff	800/5
#define zeroCyclesOn	350/5
#define zeroCyclesOff	600/5
#define resetCycles		60000/5	// Must be at least 50u, use 60u

// #define ONE

volatile register uint32_t __R30;
volatile register uint32_t __R31;

void main(void)
{
	/* Clear SYSCFG[STANDBY_INIT] to enable OCP master port */
	CT_CFG.SYSCFG_bit.STANDBY_INIT = 0;

	uint32_t i;
	// Select which pins to output to.  These are all on pru1_1
	uint32_t gpio = P9_14;
	
	for(i=0; i<STR_LEN*3*8; i++) {
#ifdef ONE
		__R30 |= gpio;		// Set the GPIO pin to 1
		__delay_cycles(oneCyclesOn-1);
		__R30 &= ~gpio;	// Clear the GPIO pin
		__delay_cycles(oneCyclesOff-2);
#else
		__R30 |= gpio;		// Set the GPIO pin to 1
		__delay_cycles(zeroCyclesOn-1);
		__R30 &= ~gpio;		// Clear the GPIO pin
		__delay_cycles(zeroCyclesOff-2);
#endif
	}
	// Send Reset
	__R30 &= ~(gpio);	// Clear the GPIO pin
	__delay_cycles(resetCycles);
	
	__halt();
}
