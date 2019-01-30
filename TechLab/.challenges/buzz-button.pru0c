#include <stdint.h>
#include <pru_cfg.h>
#include <pru_ctrl.h>
#include <stddef.h>
#include <rsc_types.h>

volatile register unsigned int __R30;
volatile register unsigned int __R31;

#pragma DATA_SECTION(init_pins, ".init_pins")
#pragma RETAIN(init_pins)
const char init_pins[] =
	"/sys/devices/platform/ocp/ocp:P1_33_pinmux/state\0pruout\0" \
	"/sys/devices/platform/ocp/ocp:P2_30_pinmux/state\0pruout\0" \
	"/sys/devices/platform/ocp/ocp:P1_29_pinmux/state\0pruin\0" \
	"\0\0";

void main(void) {
        /* Toggle GPIO outputs 1 and 3 at 400Hz when GPIO input 7 is low */
	/* On TechLab, output 1 is the red in the RGB LED */
	/* On TechLab, output 3 is the buzzer */
	/* On TechLab, input 7 is the R button */
        while(1) {
		if(__R31 & (1<<7)) {
			/* Clear outputs */
			__R30 &= ~((1<<3)|(1<<1));
		} else {
			/* Toggle outputs */
			__R30 |= ((1<<3)|(1<<1));
			__delay_cycles(500000);
			__R30 ^= ((1<<3)|(1<<1));
			__delay_cycles(500000);
		}
        }
}

struct my_resource_table {
        struct resource_table base;

        uint32_t offset[1]; /* Should match 'num' in actual definition */
};

#pragma DATA_SECTION(pru_remoteproc_ResourceTable, ".resource_table")
#pragma RETAIN(pru_remoteproc_ResourceTable)
struct my_resource_table pru_remoteproc_ResourceTable = {
        1,      /* we're the first version that implements this */
        0,      /* number of entries in the table */
        0, 0,   /* reserved, must be zero */
        0,      /* offset[0] */
};
