/*
 * See https://pub.pages.cba.mit.edu/ring/ to learn why this is important.
 *
 * Build and run with:
 * make -f /var/lib/cloud9/common/Makefile TARGET=ring.pru0
 *
 */

#include <stdint.h>
#include <pru_cfg.h>
#include <pru_ctrl.h>
#include <stddef.h>
#include <rsc_types.h>
#include <resource_table_empty.h>

volatile register unsigned int __R30;
volatile register unsigned int __R31;

void main(void) {
	/* Read GPIO input 2 and invert to GPIO output 3 */
        while(1) {
		if(__R31 & (1<<2))
			__R30 = 0;
		else
			__R30 = (1<<3);
        }
}

#pragma DATA_SECTION(init_pins, ".init_pins")
#pragma RETAIN(init_pins)
const char init_pins[] =  
	"/sys/devices/platform/ocp/ocp:P2_30_pinmux/state\0pruout\0" \
	"/sys/devices/platform/ocp/ocp:P2_32_pinmux/state\0pruin\0" \
	"\0\0";
