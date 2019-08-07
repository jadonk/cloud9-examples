////////////////////////////////////////
//	blinkExternalLED.pru0.c
//	Blinks one LED wired to P9_14 by writing to memory using the PRU
//	Wiring:	P9_14 connects to the plus lead of an LED.  The negative lead of the
//			LED goes to a 220 Ohm resistor.  The other lead of the resistor goes
//			to ground.
//	Setup:	Set the direction to out on P9_14
//	See:	prugpio.h to see to which ports the P8 and P9 pins are attached
//	PRU:	pru0
////////////////////////////////////////
#include <stdint.h>
#include <pru_cfg.h>
#include "resource_table_empty.h"
#include "prugpio.h"

volatile register unsigned int __R30;
volatile register unsigned int __R31;

void main(void) {
	// Points to the GPIO port that is used
	uint32_t *gpio1 = (uint32_t *)GPIO1;

	/* Clear SYSCFG[STANDBY_INIT] to enable OCP master port */
	CT_CFG.SYSCFG_bit.STANDBY_INIT = 0;

	while(1) {
		gpio1[GPIO_SETDATAOUT]   = P9_14;	// Turn the USR1 LED on
		__delay_cycles(500000000/5);		// Wait 1/2 second
		gpio1[GPIO_CLEARDATAOUT] = P9_14;	// Off
		__delay_cycles(500000000/5); 
	}
	__halt();
}


// Set direction of P9_14 (which is port 1 pin 18)
#pragma DATA_SECTION(init_pins, ".init_pins")
#pragma RETAIN(init_pins)
const char init_pins[] =  
	"/sys/class/gpio/gpio50/direction\0out\0" \
	"/sys/devices/platform/ocp/ocp:P9_14_pinmux/state\0gpio\0" \
	"\0\0";

// The export doesn't have to be done on the Black since 
//	GPIOs are already exported
	// "/sys/class/gpio/export\0 177\0" 
