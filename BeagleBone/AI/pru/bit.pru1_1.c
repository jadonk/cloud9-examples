////////////////////////////////////////
//	flipbit.pru1_1.c
//	Demo of shared memory
//	Usage:	This takes the first word of SHARED_RAM and flips every other bit
//				over and over.  Works for DMEM0 and DMEM1, but not SRAM.
//	Wiring:	None
//	Setup:	Run this on a PRU and run bitflip.arm.c on the ARM using /dev/uio0.
//	See:	 
//	PRU:	pru1_0 or pru1_1
////////////////////////////////////////
#include <stdint.h>
#include <pru_cfg.h>
#include <pru_ctrl.h>
#include <stddef.h>
#include <rsc_types.h>
#include "resource_table_empty.h"
#include "init_pins_empty.h"

#define PRU_DMEM0 __far __attribute__((cregister("PRU_DMEM_0_1",  near)))
#define PRU_DMEM1 __far __attribute__((cregister("PRU_DMEM_1_0",  near)))
#define PRU_SRAM  __far __attribute__((cregister("PRU_SHAREDMEM", near)))

/* NOTE:  Allocating shared_x to PRU Shared Memory means that other PRU cores on
 *        the same subsystem must take care not to allocate data to that memory.
 *		  Users also cannot rely on where in shared memory these variables are placed
 *        so accessing them from another PRU core or from the ARM is an undefined behavior.
 */
// volatile uint32_t shared_0;
PRU_DMEM0 volatile uint32_t shared_1;
PRU_DMEM1 volatile uint32_t shared_2;
PRU_SRAM  volatile uint32_t shared_3;

void main(void) {
	uint32_t value = 0;

	/* Set the shared_1 value to 0 */
	shared_1 =  0;

	while(1) {
		/* Look for the ARM to modify the SHARED_RAM value */
		if(value != shared_1) {
			/* Flip every other bit and write the value back */
			value = shared_1;
			value ^= 0xAAAAAAAA;
			shared_1 = value;
		}
	}
}
