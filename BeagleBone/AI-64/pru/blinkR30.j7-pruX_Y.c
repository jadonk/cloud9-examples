#include <stdint.h>
#include "resource_table_empty.h"
#include "prugpio.h"

volatile register unsigned int __R30;
volatile register unsigned int __R31;

void main(void) {
	//uint32_t gpio = P8_04;

	while(1) {
		__R30 = 0xFFFFFF;		// Set GPIO pins
		__delay_cycles(500000000/5);    // Wait 1/2 second
		__R30 = 0;			// Clear GPIO pins
		__delay_cycles(500000000/5); 
		}
	__halt();
}

// Sets pinmux
#pragma DATA_SECTION(init_pins, ".init_pins")
#pragma RETAIN(init_pins)
const char init_pins[] =  
	"\0\0";
