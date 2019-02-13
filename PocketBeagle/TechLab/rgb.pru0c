#include <stdint.h>
#include <pru_cfg.h>
#include <pru_ctrl.h>
#include <stddef.h>
#include <rsc_types.h>

#define	INS_PER_US 200           // 5ns per instruction
#define INS_PER_DELAY_LOOP 2	 // two instructions per delay loop
#define DELAY_CYCLES_US (INS_PER_US / INS_PER_DELAY_LOOP)

#define GPIO1 0x4804C000
#define GPIO_CLEARDATAOUT 0x190
#define GPIO_SETDATAOUT 0x194

/* GPIO1 */
#define P2_1 (1<<18)
#define USR0 (1<<21)
#define USR1 (1<<22)
#define USR2 (1<<23)
#define USR3 (1<<24)
unsigned int volatile * const GPIO1_CLEAR = (unsigned int *) (GPIO1 + GPIO_CLEARDATAOUT);
unsigned int volatile * const GPIO1_SET = (unsigned int *) (GPIO1 + GPIO_SETDATAOUT);

/* PRU GPIO */
volatile register unsigned int __R30;
volatile register unsigned int __R31;
#define P1_36 (1<<0)
#define P1_33 (1<<1)

#define DECAY_RATE 75
#define DELAY_CYCLES 2
#define RED 1
#define GREEN 2
#define BLUE 3
#define WHITE 4

const int decay = DECAY_RATE;

#pragma DATA_SECTION(init_pins, ".init_pins")
#pragma RETAIN(init_pins)
const char init_pins[] =
	"/sys/class/leds/beaglebone:green:usr3/trigger\0none\0" \
	"/sys/devices/platform/ocp/ocp:P1_36_pinmux/state\0pruout\0" \
	"/sys/devices/platform/ocp/ocp:P1_33_pinmux/state\0pruout\0" \
	"/sys/devices/platform/ocp/ocp:P2_01_pinmux/state\0gpio\0" \
	"/sys/class/gpio/gpio50/direction\0out\0" \
	"\0\0";

void main(void) {
	int i, j;
	int state = RED;

	/* Clear SYSCFG[STANDBY_INIT] to enable OCP master port */
	CT_CFG.SYSCFG_bit.STANDBY_INIT = 0;

	/* clear */
	*GPIO1_CLEAR = (P2_1 | USR3);
	__R30 &= ~(P1_33 | P1_36);
			
	while(1) {
		for(j = 0; j < 10000; j++) {
			switch(state) {
				case RED:
					*GPIO1_SET = (USR3);
					__R30 |= (P1_33);
					break;
				case GREEN:
					*GPIO1_SET = (P2_1 | USR3);
					break;
				case BLUE:
					*GPIO1_SET = (USR3);
					__R30 |= (P1_36);
					break;
				default:
				case WHITE:
					*GPIO1_SET = (P2_1 | USR3);
					__R30 |= (P1_33 | P1_36);
					break;
			}
			
			/* Delay j times */
			for(i = 0; i < j; i++) __delay_cycles(DELAY_CYCLES);
			
			/* Clear all LEDs */
			*GPIO1_CLEAR = (P2_1 | USR3);
			__R30 &= ~(P1_33 | P1_36);
			
			/* Delay 100000-j times */
			for(i = 0; i < 10000-j; i++) __delay_cycles(DELAY_CYCLES);
		}

		switch(state) {
			case RED:
				state = GREEN;
				break;
			case GREEN:
				state = BLUE;
				break;
			case BLUE:
				state = WHITE;
				break;
			default:
			case WHITE:
				state = RED;
				break;
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
	1,	/* we're the first version that implements this */
	0,	/* number of entries in the table */
	0, 0,	/* reserved, must be zero */
	0,	/* offset[0] */
};
