////////////////////////////////////////
//	pruspeak.pru0.c
//	Uses rpmsg accept messages to /dev/rpmsg_pru30 by the ARM
//	Usage:	
//	Wiring:	
//	Setup:	
//	See:	https://botspeak.org/ and https://beagleboard.org/pruspeak
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

volatile register uint32_t __R30;
volatile register uint32_t __R31;

/* Host-0 Interrupt sets bit 30 in register R31 */
#define HOST_INT		((uint32_t) 1 << 30)	

/* The PRU-ICSS system events used for RPMsg are defined in the Linux device tree
 * PRU0 uses system event 16 (To ARM) and 17 (From ARM)
 * PRU1 uses system event 18 (To ARM) and 19 (From ARM)
 * Be sure to change the values in resource_table_0.h too.
 */
#define TO_ARM_HOST		16	
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

/* PRU GPIO */
volatile register unsigned int __R30;
volatile register unsigned int __R31;

/* rpmsg buffer */
char payload[RPMSG_BUF_SIZE];

/* Botspeak globals */
#define PROG_SIZE       256
#define DATA_SIZE	32
#define OPCODE_MASK     0xFF000000
#define OPCODE_SHIFT	24
#define REG_TYPE_MASK	0x0F00
#define OPERAND1_MASK	0x00FFF000
#define OPERAND1_SHIFT	12
#define OPERAND2_MASK	0x00000FFF
#define OPERAND2_SHIFT  0
#define OPCODE_ADD      0x00	// ADD test,2		test=test+2
#define OPCODE_SUB      0x01	// SUB test,1		test=test-1
#define OPCODE_MUL      0x02	// MUL test,AI[0]	test=test*(value of analog in channel 0)
#define OPCODE_DIV      0x03	// DIV test,3   	test=test/3
#define OPCODE_MOD      0x04	// MOD 5,2      	Gets the remainder of 5/2	
#define OPCODE_AND      0x05	// AND test,AI[0]	bitwise AND	
#define OPCODE_OR       0x07	// OR test,AI[0]	Bitwise OR
#define OPCODE_NOT      0x07	// NOT test,AI[0]	returns resulting boolean
				//              	test = (test != AI[0])	
#define OPCODE_EQL      0x08	// EQL test,AI[0]	returns resulting boolean
                               	//              	test = (test == AI[0])
#define OPCODE_GRT      0x09	// GRT test,AI[0]	returns resulting boolean
                               	//              	test = (test > AI[0])	
#define OPCODE_GRE	0x0A	// GRE test,AI[0]	returns resulting boolean
                               	//              	test = (test >= AI[0])	
#define OPCODE_LET      0x0B	// LET test,AI[0]	returns resulting boolean
                               	//              	test = (test < AI[0])
#define OPCODE_LEE      0x0C	// LEE test,AI[0]	returns resulting boolean
                               	//              	test = (test <= AI[0])	
#define OPCODE_BSL      0x0D	// BSL test,2		bitwise left shift	
#define OPCODE_BSR      0x0E	// BSR test,2		bitwise right shift	
#define OPCODE_GOTO	0x0F	// GOTO 2		Will jump to line 2 of script (line indexing starts at 0)
#define OPCODE_WAIT	0x10	// WAIT 120		waits 120 msec	
#define OPCODE_GET	0x11	// GET AI[2]		Get the value of analog channel 2
#define OPCODE_SET	0x12	// SET DIO[1],1		Sets a variable to a value
#define OPCODE_IF	0x13	// (var conditional var) goto loc
				// IF (test < 1) GOTO 3	jumps to line 3 if test is less than 1. 
				// If test >= 1, it goes to the next line (Note, you need the spaces in the parentheses)
				// This is implemented as 2 instructions with this opcode being a conditional goto
#define OPCODE_CALL	0x14	// RUN&WAIT Sub		Runs script starting at the label Sub and waits until the script is done
#define OPCODE_RET	0x15	// ENDSCRIPT
				
// Non opcode instructions
				// RUN 0		Runs existing script starting at line 0
				// DEBUG 0		Runs current script (from the beginning) in debug mode (outputs values)	
				// LBL			Allocate variable to store current program_used
				
#define REG_VARIABLE	0x0	// GET test		returns value of variable
#define REG_AO		0x1	// SET AO[1],0.5	Analog out channel 1 50%	
#define REG_TMR		0x2	// GET TMR[1]		Gets the value of Timer 1	
#define REG_DIO		0x3	// GET DIO[1]		Get the value of DIO line 1
				// SET DIO[1]		Set the value of DIO line 1
#define REG_AI		0x4	// GET AI[2]		Get voltage on analog in channel 2	
#define REG_SERVO	0x5	// SET SERVO[2],test	sets PWM[2] to duty of test (value between 0 and 1.5)
#define REG_PWM		0x6	// SET PWM[0],50	Set pulse width modulation on chan 0 to 50%	
#define REG_VER		0x7	// GET VER		returns version of VM

uint32_t program[PROG_SIZE];
uint32_t data[DATA_SIZE];
uint32_t reg = 0;
uint32_t ins_ptr = 0;
uint32_t program_used = 0;
uint32_t data_used = 0;
struct identifier_list_element {
	char * string;
	uint32_t index;
	void * next;
} identifier_head;
int script_mode = 0;
int debug_mode = 0;
int run_mode = 0;

uint32_t interpret_payload(char * payload, int len);
void execute(uint32_t ins);
void update_timers();

void main(void)
{
	struct pru_rpmsg_transport transport;
	uint16_t src, dst, len;
	volatile uint8_t *status;
	uint32_t ins;
	
	/* Initialize some globals */
	identifier_head.next = 0;

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
	
	/* Main loop */
	while (1) {
		/* Check bit 30 of register R31 to see if the ARM has kicked us */
		if (__R31 & HOST_INT) {
			/* Clear the event status */
			CT_INTC.SICR_bit.STS_CLR_IDX = FROM_ARM_HOST;
			/* Receive all available messages, multiple messages can be sent per kick */
			if (pru_rpmsg_receive(&transport, &src, &dst, payload, &len) == PRU_RPMSG_SUCCESS) {
				/* Process message */
				ins = interpret_payload(payload, len);
				if (script_mode) {
					if (program_used < PROG_SIZE) {
						program[program_used] = ins;
						program_used++;
					}
				} else {
					execute(ins);
					if (debug_mode) {
						pru_rpmsg_send(&transport, dst, src, "A", 2);
					}
				}
			}
		}

		/* Continue script execution */
		if (run_mode && (ins_ptr < program_used)) {
			execute(program[ins_ptr]);
			if (debug_mode) {
				pru_rpmsg_send(&transport, dst, src, "B", 2);
			}
		}

		/* Perform software-based PWM, check timers, etc. */
		update_timers();
	}
}

uint32_t interpret_payload(char * payload, int len) {
	return(0);
}

void execute(uint32_t ins) {
	
}

void update_timers() {
	
}

// Sets pinmux
#pragma DATA_SECTION(init_pins, ".init_pins")
#pragma RETAIN(init_pins)
const char init_pins[] =
	"\0\0";
