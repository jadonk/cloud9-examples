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
#include "tsc_adc.h"
#include "soc_AM335x.h"

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
	uint32_t x;

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
				x = TSCADCFIFOADCDataRead(SOC_ADC_TSC_0_REGS, 0);
				sprintf(payload, "0x%08x\n", x);
				len = strlen(payload);
				pru_rpmsg_send(&transport, dst, src, payload, len);
			}
		}
	}
}

/* ADC is configured */
static void ADCConfigure(void)
{
    /* Enable the clock for touch screen */
    //TSCADCModuleClkConfig();

    //TSCADCPinMuxSetUp();

    /* Configures ADC to 3Mhz */
    //TSCADCConfigureAFEClock(SOC_ADC_TSC_0_REGS, 24000000, 3000000);

    /* Enable Transistor bias */
    //TSCADCTSTransistorConfig(SOC_ADC_TSC_0_REGS, TSCADC_TRANSISTOR_ENABLE);

    //TSCADCStepIDTagConfig(SOC_ADC_TSC_0_REGS, 1);

    /* Disable Write Protection of Step Configuration regs*/
    //TSCADCStepConfigProtectionDisable(SOC_ADC_TSC_0_REGS);

    /* Configure ADC to Single ended operation mode */
    //TSCADCTSStepOperationModeControl(SOC_ADC_TSC_0_REGS,
                                  //TSCADC_SINGLE_ENDED_OPER_MODE, 0);

    /* Configure step to select Channel, refernce voltages */
    //TSCADCTSStepConfig(SOC_ADC_TSC_0_REGS, stepSel, TSCADC_NEGATIVE_REF_VSSA,
                    //TSCADC_POSITIVE_INP_CHANNEL1, TSCADC_NEGATIVE_INP_CHANNEL1,
                    //TSCADC_POSITIVE_REF_VDDA);

    /* Configure step 1 for channel 1(AN0)*/
    //StepConfigure(0, TSCADC_FIFO_0, TSCADC_POSITIVE_INP_CHANNEL1);

    /* Configure step 2 for channel 2(AN1)*/
    //StepConfigure(1, TSCADC_FIFO_1, TSCADC_POSITIVE_INP_CHANNEL2);

    /* General purpose inputs */
    //TSCADCTSModeConfig(SOC_ADC_TSC_0_REGS, TSCADC_GENERAL_PURPOSE_MODE);

    /* Enable step 1 */
    //TSCADCConfigureStepEnable(SOC_ADC_TSC_0_REGS, 1, 1);

    /* Enable step 2 */
    //TSCADCConfigureStepEnable(SOC_ADC_TSC_0_REGS, 2, 1);

    /* Clear the status of all interrupts */
    //CleanUpInterrupts();

    /* End of sequence interrupt is enable */
    //TSCADCEventInterruptEnable(SOC_ADC_TSC_0_REGS, TSCADC_END_OF_SEQUENCE_INT);

    /* Enable the TSC_ADC_SS module*/
    //TSCADCModuleStateSet(SOC_ADC_TSC_0_REGS, TSCADC_MODULE_ENABLE);
}

// Sets pinmux
#pragma DATA_SECTION(init_pins, ".init_pins")
#pragma RETAIN(init_pins)
const char init_pins[] =
	"/sys/bus/platform/drivers/ti_am3359-tscadc/unbind\000044e0d000.tscadc\0"
	"\0\0";
