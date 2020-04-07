////////////////////////////////////////
//	blinkInternalLED.pru0.c
//	Blinks two of the bulit in USR LEDs using the PRU
//	Wiring:	None
//	Setup:	Turn off the USR LEDs triggers
//	See:	prugpio.h to see to which ports the USR LEDs are attached
//	PRU:	Any
////////////////////////////////////////
#include <stdint.h>
#include <pru_cfg.h>
#include "resource_table_empty.h"
#include "prugpio.h"

volatile register unsigned int __R30;
volatile register unsigned int __R31;

void main(void) {
	// Points to the two GPIO ports that are used
	uint32_t *gpio1 = (uint32_t *)GPIO1;

	/* Clear SYSCFG[STANDBY_INIT] to enable OCP master port */
	CT_CFG.SYSCFG_bit.STANDBY_INIT = 0;

	while(1) {
		gpio1[GPIO_SETDATAOUT]   = USR1;	// Turn the USR1 LED on
		gpio1[GPIO_CLEARDATAOUT] = USR2;	// Turn USR2 LED off
		
		__delay_cycles(500000000/5);	 // Wait 1/2 second
		
		gpio1[GPIO_CLEARDATAOUT] = USR1;	// Off
		gpio1[GPIO_SETDATAOUT]   = USR2;	// On
        
		__delay_cycles(500000000/5); 
	}
	__halt();
}

// Turns off triggers
#pragma DATA_SECTION(init_pins, ".init_pins")
#pragma RETAIN(init_pins)
const char init_pins[] =  
	"/sys/class/leds/beaglebone:green:usr1/trigger\0none\0" \
	"/sys/class/leds/beaglebone:green:usr2/trigger\0none\0" \
	"\0\0";
