////////////////////////////////////////
//	halt.pru0.c
//	Just halts
//	Wiring:	None
//	Setup:	
//	See:	
//	PRU:	Any
////////////////////////////////////////
#include <stdint.h>
#include <pru_cfg.h>
#include "resource_table_empty.h"
#include "prugpio.h"

volatile register unsigned int __R30;
volatile register unsigned int __R31;

void main(void) {
	__halt();
}
