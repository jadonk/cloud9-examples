// Demo of shared memory

#include <stdint.h>
#include <pru_cfg.h>
#include <pru_ctrl.h>
#include <stddef.h>
#include <rsc_types.h>

#define SHARED_RAM_ADDRESS 0x10000
unsigned int volatile __far * const SHARED_RAM = (unsigned int *) (SHARED_RAM_ADDRESS);

void main(void) {
	unsigned int value = 0;

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

// Define an empty init_pins table so write_init_pins won't complain
#pragma DATA_SECTION(init_pins, ".init_pins")
#pragma RETAIN(init_pins)
const char init_pins[] =
	"\0\0";

// Define an empty resource table so remoteproc won't complain
struct my_resource_table {
	struct resource_table base;
	uint32_t offset[1]; /* Should match 'num' in actual definition */
};
#pragma DATA_SECTION(pru_remoteproc_ResourceTable, ".resource_table")
#pragma RETAIN(pru_remoteproc_ResourceTable)
struct my_resource_table pru_remoteproc_ResourceTable = {
	1,	/* we're the first version that implements this */
	0,	/* number of entries in the table */
	0, 0,	/* reserved, must be zero */
	0,	/* offset[0] */
};
