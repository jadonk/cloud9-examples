// Demo of shared memory

#include <stdint.h>
#include <pru_cfg.h>
#include <pru_ctrl.h>
#include <stddef.h>
#include <rsc_types.h>
#include "resource_table_empty.h"
#include "init_pins_empty.h"

#define PRUN 1_1

#define SHARED_RAM_ADDRESS 0x10000
unsigned int volatile __far * const SHARED_RAM = (unsigned int *) (SHARED_RAM_ADDRESS);

volatile register unsigned int __R30;
volatile register unsigned int __R31;

void main(void) {
	unsigned int value = 0;

	/* Clear SYSCFG[STANDBY_INIT] to enable OCP master port */
	CT_CFG.SYSCFG_bit.STANDBY_INIT = 0;

	/* Set the SHARED_RAM value to 0 */
	*SHARED_RAM = 0;

	while(1) {
		/* Look for the ARM to modify the SHARED_RAM value */
		if(value != *SHARED_RAM) {
			/* Flip every other bit and write the value back */
			value = *SHARED_RAM;
			value ^= 0xAAAAAAAA;
			*SHARED_RAM = value;
		}
	}
}

