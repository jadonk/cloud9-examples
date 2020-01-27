////////////////////////////////////////
//	rgbLEDrpmsg.pru0
//	Uses rpmsg to control the NeoPixels via /dev/rpmsg_pru30 on the ARM
//	Usage:	echo index R G B > /dev/rpmsg_pru30 to set the color at the given index
//			echo -1 0 0 0    > /dev/rpmsg_pro30 to update the string
//			echo 0 0xf0 0 0  > /dev/rpmsg_pru30 Turns pixel 0 to Red
//			neopixelRainbow.py to display moving rainbow pattern
//	Wiring:	The NeoPixel Data In goes to P1_36, the plus lead to P1_14 (3.3V)
//			and the ground to P2_22.  If you have more then 40 some 
//			NeoPixels you will need and external supply.
//	Setup:	config_pin P1_36 pruout
//	See:	 
//	PRU:	pru0
////////////////////////////////////////
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>			// atoi
#include <string.h>
#include <pru_cfg.h>
#include <pru_intc.h>
#include <rsc_types.h>
#include <pru_rpmsg.h>
#include "resource_table_0.h"
#include "prugpio.h"

volatile register uint32_t __R30;
volatile register uint32_t __R31;

/* Host-0 Interrupt sets bit 30 in register R31 */
#define HOST_INT			((uint32_t) 1 << 30)	

/* The PRU-ICSS system events used for RPMsg are defined in the Linux device tree
 * PRU0 uses system event 16 (To ARM) and 17 (From ARM)
 * PRU1 uses system event 18 (To ARM) and 19 (From ARM)
 * Be sure to change the values in resource_table_0.h too.
 */
#define TO_ARM_HOST			16	
#define FROM_ARM_HOST		17

/*
* Using the name 'rpmsg-pru' will probe the rpmsg_pru driver found
* at linux-x.y.z/drivers/rpmsg/rpmsg_pru.c
*/
#define CHAN_NAME			"rpmsg-pru"
#define CHAN_DESC			"Channel 30"
#define CHAN_PORT			30

/*
 * Used to make sure the Linux drivers are ready for RPMsg communication
 * Found at linux-x.y.z/include/uapi/linux/virtio_config.h
 */
#define VIRTIO_CONFIG_S_DRIVER_OK	4

/* GPIO1 */
unsigned int volatile * const GPIO1_CLEAR = (unsigned int *) (GPIO1 + GPIO_CLEARDATAOUT);
unsigned int volatile * const GPIO1_SET = (unsigned int *) (GPIO1 + GPIO_SETDATAOUT);

/* PRU GPIO */
volatile register unsigned int __R30;
volatile register unsigned int __R31;

#define DECAY_RATE 75
#define DELAY_CYCLES 2
#define RED 1
#define GREEN 2
#define BLUE 3
#define WHITE 4

void setLED(void);

char payload[RPMSG_BUF_SIZE];
int state = RED;

/*
 * main.c
 */
void main(void)
{
	struct pru_rpmsg_transport transport;
	uint16_t src, dst, len;
	volatile uint8_t *status;

	/* Allow OCP master port access by the PRU so the PRU can read external memories */
	CT_CFG.SYSCFG_bit.STANDBY_INIT = 0;
	
	setLED();

	/* Clear the status of the PRU-ICSS system event that the ARM will use to 'kick' us */
	CT_INTC.SICR_bit.STS_CLR_IDX = FROM_ARM_HOST;

	/* Make sure the Linux drivers are ready for RPMsg communication */
	status = &resourceTable.rpmsg_vdev.status;
	while (!(*status & VIRTIO_CONFIG_S_DRIVER_OK));

	/* Initialize the RPMsg transport structure */
	pru_rpmsg_init(&transport, &resourceTable.rpmsg_vring0, &resourceTable.rpmsg_vring1, TO_ARM_HOST, FROM_ARM_HOST);

	/* Create the RPMsg channel between the PRU and ARM user space using the transport structure. */
	while (pru_rpmsg_channel(RPMSG_NS_CREATE, &transport, CHAN_NAME, CHAN_DESC, CHAN_PORT) != PRU_RPMSG_SUCCESS);
	while (1) {
		/* Check bit 30 of register R31 to see if the ARM has kicked us */
		if (__R31 & HOST_INT) {
			/* Clear the event status */
			CT_INTC.SICR_bit.STS_CLR_IDX = FROM_ARM_HOST;
			/* Receive all available messages, multiple messages can be sent per kick */
			while (pru_rpmsg_receive(&transport, &src, &dst, payload, &len) == PRU_RPMSG_SUCCESS) {
			    if(!strcmp("red", payload)) {
			        state = RED;
			    } else if(!strcmp("blue", payload)) {
			        state = BLUE;
			    } else if(!strcmp("green", payload)) {
			        state = GREEN;
			    } else if(!strcmp("white", payload)) {
                    state = WHITE;			        
			    } else {
			        state = 0;
			    }
			    
			    setLED();
			}
		}
	}
}

void setLED(void) {			    
	/* Clear all LEDs */
	*GPIO1_CLEAR = (P2_1 | USR3);
	__R30 &= ~(P1_33 | P1_36);
	
	/* Turn on correct LEDs */
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
		case WHITE:
			*GPIO1_SET = (P2_1 | USR3);
			__R30 |= (P1_33 | P1_36);
			break;
		default:
			break;
	}
}
// Sets pinmux
#pragma DATA_SECTION(init_pins, ".init_pins")
#pragma RETAIN(init_pins)
const char init_pins[] =
	"/sys/class/leds/beaglebone:green:usr3/trigger\0none\0" \
	"/sys/devices/platform/ocp/ocp:P1_36_pinmux/state\0pruout\0" \
	"/sys/devices/platform/ocp/ocp:P1_33_pinmux/state\0pruout\0" \
	"/sys/devices/platform/ocp/ocp:P2_01_pinmux/state\0gpio\0" \
	"/sys/class/gpio/gpio50/direction\0out\0" \
	"\0\0";
