////////////////////////////////////////
//	blinkR30.pru0.c
//	Blinks LEDs wired to P1_36 (and others) by writing register R30 on the PRU
//	Wiring:	P1_36 connects to the plus lead of an LED.  The negative lead of the
//			LED goes to a 220 Ohm resistor.  The other lead of the resistor goes
//			to ground (P2_21).
//	Setup:	config_pin P1_36 pruout
//	See:	prugpio.h to see which pins attach to R30
//	PRU:	pru0
////////////////////////////////////////
#include <stdint.h>
#include <pru_cfg.h>
#include "resource_table_empty.h"
#include "prugpio.h"

volatile register unsigned int __R30;
volatile register unsigned int __R31;

void main(void) {
	// Select which pins to toggle.  These are all on pru1_1
	uint32_t gpio = P1_36;

	/* Clear SYSCFG[STANDBY_INIT] to enable OCP master port */
	CT_CFG.SYSCFG_bit.STANDBY_INIT = 0;

	while(1) {
		__R30 |= gpio;					// Set the GPIO pin to 1
		__delay_cycles(500000000/5);    // Wait 1/2 second
		__R30 &= ~gpio;					// Clear the GPIO pin
		__delay_cycles(500000000/5); 
		}
	__halt();
}

// Sets pinmux
#pragma DATA_SECTION(init_pins, ".init_pins")
#pragma RETAIN(init_pins)
const char init_pins[] =  
	"/sys/devices/platform/ocp/ocp:P1_36_pinmux/state\0pruout\0" \
	"\0\0";
