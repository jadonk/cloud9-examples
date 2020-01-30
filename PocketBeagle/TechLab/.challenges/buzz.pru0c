#include <stdint.h>
#include <pru_cfg.h>
#include <pru_ctrl.h>
#include <stddef.h>
#include <rsc_types.h>

#define INS_PER_US 200           // 5ns per instruction
#define INS_PER_DELAY_LOOP 2     // two instructions per delay loop
#define DELAY_CYCLES    1250*(INS_PER_US / INS_PER_DELAY_LOOP)  // About 2*400Hz

volatile register unsigned int __R30;
volatile register unsigned int __R31;

#pragma DATA_SECTION(init_pins, ".init_pins")
#pragma RETAIN(init_pins)
const char init_pins[] =  
	"/sys/devices/platform/ocp/ocp:P2_30_pinmux/state\0pruout\0" \
	"\0\0";

void main(void) {
	int i;
	/* On TechLab, output 1 is the red in the RGB LED */
	/* On TechLab, output 3 is the buzzer */
	/* On TechLab, input 7 is the R button */
	
        /* Toggle GPIO output 3 at 400Hz for 0.5 second */
        for(i=0; i<200; i++) {
		/* Toggle output */
		__R30 |= (1<<3);
		__delay_cycles(DELAY_CYCLES);
		__R30 ^= (1<<3);
		__delay_cycles(DELAY_CYCLES);
        }
	
        /* Toggle GPIO output 3 at 800Hz for 0.5 second */
        for(i=0; i<400; i++) {
		/* Toggle output */
		__R30 |= (1<<3);
		__delay_cycles(DELAY_CYCLES/2);
		__R30 ^= (1<<3);
		__delay_cycles(DELAY_CYCLES/2);
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
