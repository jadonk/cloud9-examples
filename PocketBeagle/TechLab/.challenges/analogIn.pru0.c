////////////////////////////////////////
//	analogIn.pru0.c
//	Reads AIN0 and outputs to /dev/rpmsg_pru30 when sent a message
//	Usage:	echo x > /dev/rpmsg_pru30, cat /dev/rpmsg_pru30
//	Wiring:	PocketBeagle + TechLab
//	Setup:	tested with 4.14.108-ti-r124 kernel
//	See:	 
//	PRU:	pru0
////////////////////////////////////////
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <pru_cfg.h>
#include <pru_intc.h>
#include <rsc_types.h>
#include <pru_rpmsg.h>
#include "resource_table_0.h"
#include "prugpio.h"
#include "hw_types.h"
#include "tsc_adc.h"
#include "soc_AM335x.h"
#include "hw_control_AM335x.h"
#include "hw_cm_per.h"
#include "hw_cm_wkup.h"


static void ADCConfigure(void);

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
#define FROM_ARM_HOST			17

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

char payload[RPMSG_BUF_SIZE];

/*
 * main.c
 */
void main(void)
{
	struct pru_rpmsg_transport transport;
	uint16_t src, dst, len;
	volatile uint8_t *status;
	unsigned int i, count, data, sample;

	ADCConfigure();

	/* Allow OCP master port access by the PRU so the PRU can read external memories */
	CT_CFG.SYSCFG_bit.STANDBY_INIT = 0;
	
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
				/* Start step */
				HWREG(SOC_ADC_TSC_0_REGS + TSC_ADC_SS_STEPENABLE) = 0xfe;

				/* Wait for interrupt */
				while (!(HWREG(SOC_ADC_TSC_0_REGS + TSC_ADC_SS_IRQSTATUS)&0x02));

				/* Clear interrupt */
				HWREG(SOC_ADC_TSC_0_REGS + TSC_ADC_SS_IRQSTATUS) = 0x02;

				sample = 0xFFFFFFFF;

				count = HWREG(SOC_ADC_TSC_0_REGS + TSC_ADC_SS_FIFOCOUNT(0));
				//sample = count;
				for (i = 0; i < count; i++) {
					data = HWREG(SOC_ADC_TSC_0_REGS + TSC_ADC_SS_FIFODATA(0));
					if ((data & 0x000F0000) == 0) {
						/* if channel == 0 */
						sample = data & 0xFFF;
					}
				}
				memcpy(payload, "\0\0\0\0\0\0\0\0\0\0", 10);
				ltoa((long)sample, payload);
				//len = strlen(payload) + 1;
				pru_rpmsg_send(&transport, dst, src, payload, 10);
			}
		}
	}
}

static void ADCConfigure(void)
{
	unsigned int i, count, data;

	/* Enable ADC module clock */
	HWREG(SOC_CM_WKUP_REGS + CM_WKUP_ADC_TSC_CLKCTRL) = 0x02;

	/* Disable ADC module for configuration */
	HWREG(SOC_ADC_TSC_0_REGS + TSC_ADC_SS_CTRL) &= ~0x01;

	/* fs = 24MHz / ((CLKDIV+1)*2*Channels*(OpenDly+Average*(14+SampleDly)))
	 *    = 53.57kHz
	 * CLKDIV = 0
	 * Channels = 1
	 * Average = 16
	 * OpenDly = 0
	 * SampleDly = 0
	 */
	HWREG(SOC_ADC_TSC_0_REGS + TSC_ADC_SS_ADC_CLKDIV) = 0;

	HWREG(SOC_ADC_TSC_0_REGS + TSC_ADC_SS_ADCRANGE) = 0xFFF << 16;

	/* Disable all steps for now */
	HWREG(SOC_ADC_TSC_0_REGS + TSC_ADC_SS_STEPENABLE) &= 0xFF;

	/* Unlock step configuration */
	HWREG(SOC_ADC_TSC_0_REGS + TSC_ADC_SS_CTRL) |= 0x04;

	/* Step 1 config: SW mode, one shot mode, fifo 0, channel 0 */
	HWREG(SOC_ADC_TSC_0_REGS + TSC_ADC_SS_STEPCONFIG(0)) = 0x00000000;
	HWREG(SOC_ADC_TSC_0_REGS + TSC_ADC_SS_STEPDELAY(0)) = 0xFF000000;

	/* Enable channel ID tag */
	HWREG(SOC_ADC_TSC_0_REGS + TSC_ADC_SS_CTRL) |= 0x02;

	/* Clear end-of-sequence interrupt */
	HWREG(SOC_ADC_TSC_0_REGS + TSC_ADC_SS_IRQSTATUS) = 0x02;

	/* Enable end-of-sequence interrupt */
	HWREG(SOC_ADC_TSC_0_REGS + TSC_ADC_SS_IRQENABLE_SET) = 0x02;

	/* Lock step configuration */
	HWREG(SOC_ADC_TSC_0_REGS + TSC_ADC_SS_CTRL) &= ~0x04;

	/* Empty FIFO 0 */
	count = HWREG(SOC_ADC_TSC_0_REGS + TSC_ADC_SS_FIFOCOUNT(0));
	for (i = 0; i < count; i++) {
		data = HWREG(SOC_ADC_TSC_0_REGS + TSC_ADC_SS_FIFODATA(0));
	}

	/* Enable ADC module */
	HWREG(SOC_ADC_TSC_0_REGS + TSC_ADC_SS_CTRL) |= 0x01;
}

// Sets pinmux
#pragma DATA_SECTION(init_pins, ".init_pins")
#pragma RETAIN(init_pins)
const char init_pins[] =
	"/sys/bus/platform/drivers/ti_am3359-tscadc/unbind\00044e0d000.tscadc\0"
	"\0\0";
