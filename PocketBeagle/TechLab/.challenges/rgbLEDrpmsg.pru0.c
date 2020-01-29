////////////////////////////////////////
//	rgbLEDrpmsg.pru0
//	Uses rpmsg accept messages to /dev/rpmsg_pru30 by the ARM
//	Usage:	echo green > /dev/rpmsg_pru30 to set the TechLab RGB LED green
//	Wiring:	PocketBeagle + TechLab
//	Setup:	tested with 4.14.108-ti-r124 kernel
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
unsigned int volatile * const GPIO1_CLEAR = ((unsigned int *) GPIO1) + (GPIO_CLEARDATAOUT);
unsigned int volatile * const GPIO1_SET = ((unsigned int *) GPIO1) + (GPIO_SETDATAOUT);

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
volatile int state = RED;

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
			    /* Set the state based on the payload */
			    if(!strncmp("red\n", payload, 1)) {
				    pru_rpmsg_send(&transport, dst, src, "r", 2);
			        state = RED;
			    } else if(!strncmp("blue\n", payload, 1)) {
				    pru_rpmsg_send(&transport, dst, src, "b", 2);
			        state = BLUE;
			    } else if(!strncmp("green\n", payload, 1)) {
				    pru_rpmsg_send(&transport, dst, src, "g", 2);
			        state = GREEN;
			    } else if(!strncmp("white\n", payload, 1)) {
				    pru_rpmsg_send(&transport, dst, src, "w", 2);
                    state = WHITE;			        
			    } else {
				    pru_rpmsg_send(&transport, dst, src, payload, len);
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
