#include <stdint.h>
#include <stddef.h>
#include <rsc_types.h>
#include "resource_table_empty.h"
#include "prugpio.h"

volatile register unsigned int __R30;
volatile register unsigned int __R31;

void main(void) {
        while(1) {
		if(__R31 & P8_11)
			__R30 = 0;
		else
			__R30 = P8_04;
        }
}
