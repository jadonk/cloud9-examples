#include <stdint.h>
#include <pru_cfg.h>
#include "resource_table_empty.h"
#include "prugpio.h"

#define	PRUN 1_1

volatile register unsigned int __R30;
volatile register unsigned int __R31;

void main(void) {
	int i;
	uint32_t *gpio3 = (uint32_t *)GPIO3;
	uint32_t *gpio5 = (uint32_t *)GPIO5;

	/* Clear SYSCFG[STANDBY_INIT] to enable OCP master port */
	CT_CFG.SYSCFG_bit.STANDBY_INIT = 0;

	for(i=0; i<100; i++) {
		gpio5[GPIO_SETDATAOUT]   = USR1;	// Turn the USR1 LED on
		gpio3[GPIO_CLEARDATAOUT] = USR2;	// Turn USR2 LED off
		
		__delay_cycles(500000000/5);	 // Wait 1/2 second
		
		gpio5[GPIO_CLEARDATAOUT] = USR1;	// Off
        gpio3[GPIO_SETDATAOUT]   = USR2;	// On
        
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

