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

#define VERSION			0x00000001
#define DELAY_CYCLES_PER_MS	200000

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

/* Botspeak globals */
#define PROG_SIZE       256
#define DATA_SIZE	32
#define STACK_SIZE	8
#define OPCODE_MASK     0xFF000000
#define OPCODE_SHIFT	24
#define OPERAND1_TMASK	0x00F00000
#define OPERAND1_TSHIFT	20
#define OPERAND1_MASK	0x000FF000
#define OPERAND1_SHIFT	12
#define OPERAND2_TMASK	0x00000F00
#define OPERAND2_TSHIFT	8
#define OPERAND2_MASK	0x000000FF
#define OPERAND2_SHIFT  0
const char opcodes[] = \
//	 0    1    2    3    4    5    6    7    8    9    A    B    C    D    E    F
	"NOP  ADD  SUB  MUL  DIV  MOD  AND  OR   NOT  EQL  GRT  GRE  LET  LEE  BSL  BSR  "\
	"GOTO WAIT GET  SET  IF   CALL RET  RUN  DBG  ";
#define OPCODE_NOP	0x00
#define OPCODE_ADD      0x01	// ADD test,2		test=test+2
#define OPCODE_SUB      0x02	// SUB test,1		test=test-1
#define OPCODE_MUL      0x03	// MUL test,AI[0]	test=test*(value of analog in channel 0)
#define OPCODE_DIV      0x04	// DIV test,3   	test=test/3
#define OPCODE_MOD      0x05	// MOD 5,2      	Gets the remainder of 5/2	
#define OPCODE_AND      0x06	// AND test,AI[0]	bitwise AND	
#define OPCODE_OR       0x07	// OR test,AI[0]	Bitwise OR
#define OPCODE_NOT      0x08 	// NOT test,AI[0]	returns resulting boolean
			        //              	test = (test != AI[0])	
#define OPCODE_EQL      0x09	// EQL test,AI[0]	returns resulting boolean
                               	//              	test = (test == AI[0])
#define OPCODE_GRT      0x0A	// GRT test,AI[0]	returns resulting boolean
                               	//              	test = (test > AI[0])	
#define OPCODE_GRE	0x0B	// GRE test,AI[0]	returns resulting boolean
                               	//              	test = (test >= AI[0])	
#define OPCODE_LET      0x0C	// LET test,AI[0]	returns resulting boolean
                               	//              	test = (test < AI[0])
#define OPCODE_LEE      0x0D	// LEE test,AI[0]	returns resulting boolean
                              	//              	test = (test <= AI[0])	
#define OPCODE_BSL      0x0E	// BSL test,2		bitwise left shift	
#define OPCODE_BSR      0x0F	// BSR test,2		bitwise right shift	
#define OPCODE_GOTO	0x10	// GOTO 2		Will jump to line 2 of script (line indexing starts at 0)
#define OPCODE_WAIT	0x11	// WAIT 120		waits 120 msec	
#define OPCODE_GET	0x12	// GET AI[2]		Get the value of analog channel 2
#define OPCODE_SET	0x13	// SET DIO[1],1		Sets a variable to a value
#define OPCODE_IF	0x14	// (var conditional var) goto loc
				// IF (test < 1) GOTO 3	jumps to line 3 if test is less than 1. 
				// If test >= 1, it goes to the next line (Note, you need the spaces in the parentheses)
				// This is implemented as 2 instructions with this opcode being a conditional goto
#define OPCODE_CALL	0x15	// RUN&WAIT Sub		Runs script starting at the label Sub and waits until the script is done
#define OPCODE_RET	0x16	// ENDSCRIPT
#define OPCODE_RUN	0x17	// RUN 0		Runs existing script starting at line 0
#define OPCODE_DBG	0x18	// DEBUG 0		Runs current script (from the beginning) in debug mode (outputs values)	
				
// Non opcode instructions
				// LBL			Allocate variable to store current program_used

#define REG_NOP		0xF
#define REG_VARIABLE	0x0	// GET test		returns value of variable
#define REG_AO		0x1	// SET AO[1],0.5	Analog out channel 1 50%	
#define REG_TMR		0x2	// GET TMR[1]		Gets the value of Timer 1	
#define REG_DIO		0x3	// GET DIO[1]		Get the value of DIO line 1
				// SET DIO[1]		Set the value of DIO line 1
#define REG_AI		0x4	// GET AI[2]		Get voltage on analog in channel 2	
#define REG_SERVO	0x5	// SET SERVO[2],test	sets PWM[2] to duty of test (value between 0 and 1.5)
#define REG_PWM		0x6	// SET PWM[0],50	Set pulse width modulation on chan 0 to 50%	
#define REG_VER		0x7	// GET VER		returns version of VM
#define REG_IMMEDIATE	0x8

#define NIB2ASC(x)	((x)>9)?((char)((x)-10)+'A'):((char)(x)+'0')

uint32_t interpret_payload(char * payload, int len);
void execute(uint32_t ins);
void update_timers();
int32_t opfetch(uint32_t optype, uint32_t opaddr);
void opstore(uint32_t optype, uint32_t opaddr, int32_t op);

/* PRU GPIO */
volatile register unsigned int __R30;
volatile register unsigned int __R31;

/* rpmsg buffer */
char payload[RPMSG_BUF_SIZE];
struct pru_rpmsg_transport transport;
uint16_t src, dst, len;

/* Interpreter variables */
uint32_t program[PROG_SIZE];
uint32_t data[DATA_SIZE];
uint32_t stack[STACK_SIZE];
int32_t reg = 0;
uint32_t ins_ptr = 0;
uint32_t program_used = 0;
uint32_t data_used = 0;
uint32_t stack_used = 0;
struct identifier_list_element {
	char * string;
	uint32_t index;
	void * next;
} identifier_head;
int script_mode = 0;
int debug_mode = 1;
int run_mode = 0;

void main(void)
{
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
				}
			}
		}

		/* Continue script execution */
		if (ins_ptr >= program_used)
			run_mode = 0;
		if (run_mode)
			execute(program[ins_ptr]);

		/* Perform software-based PWM, check timers, etc. */
		update_timers();
	}
}

uint32_t interpret_payload(char * payload, int len) {
	const char sepchars[] = ",.;!? ";
	uint32_t ins = OPCODE_NOP << OPCODE_SHIFT;
	
	
	return(ins);
}

void execute(uint32_t ins) {
	int32_t i;
	int32_t op1 = 0;
	int32_t op2 = 0;
	uint32_t op1addr = (ins & OPERAND1_MASK) >> OPERAND1_SHIFT;
	uint32_t op2addr = (ins & OPERAND2_MASK) >> OPERAND2_SHIFT;
	uint32_t op1type = (ins & OPERAND1_TMASK) >> OPERAND1_TSHIFT;
	uint32_t op2type = (ins & OPERAND2_TMASK) >> OPERAND2_TSHIFT;

	if (run_mode && (ins_ptr < program_used)) {
		ins_ptr++;
	}

	op1 = opfetch(op1type, op1addr);
	op2 = opfetch(op2type, op2addr);

	switch ((ins & OPCODE_MASK) >> OPCODE_SHIFT) {
	default:
	case OPCODE_NOP:
		break;
	case OPCODE_ADD:
		reg = op1 + op2;
		opstore(op1type, op1addr, reg);
		break;
	case OPCODE_SUB:
		reg = op1 - op2;
		opstore(op1type, op1addr, reg);
		break;
	case OPCODE_MUL:
		reg = op1 * op2;
		opstore(op1type, op1addr, reg);
		break;
	case OPCODE_DIV:
		reg = op1 * op2;
		opstore(op1type, op1addr, reg);
		break;
	case OPCODE_MOD:
		reg = op1 * op2;
		opstore(op1type, op1addr, reg);
		break;
	case OPCODE_AND:
		reg = op1 & op2;
		opstore(op1type, op1addr, reg);
		break;
	case OPCODE_OR:
		reg = op1 | op2;
		opstore(op1type, op1addr, reg);
		break;
	case OPCODE_NOT:
		reg = op1 != op2;
		opstore(op1type, op1addr, reg);
		break;
	case OPCODE_EQL:
		reg = op1 == op2;
		opstore(op1type, op1addr, reg);
		break;
	case OPCODE_GRT:
		reg = op1 > op2;
		opstore(op1type, op1addr, reg);
		break;
	case OPCODE_GRE:
		reg = op1 >= op2;
		opstore(op1type, op1addr, reg);
		break;
	case OPCODE_LET:
		reg = op1 < op2;
		opstore(op1type, op1addr, reg);
		break;
	case OPCODE_LEE:
		reg = op1 <= op2;
		opstore(op1type, op1addr, reg);
		break;
	case OPCODE_BSL:
		reg = op1 << op2;
		opstore(op1type, op1addr, reg);
		break;
	case OPCODE_BSR:
		reg = op1 >> op2;
		opstore(op1type, op1addr, reg);
		break;
	case OPCODE_GOTO:
		ins_ptr = op1;
		break;
	case OPCODE_WAIT:
		for (i=0; i < op1; i++)
			__delay_cycles(DELAY_CYCLES_PER_MS);
		break;
	case OPCODE_GET:
		reg = op1;
		break;
	case OPCODE_SET:
		opstore(op1type, op1addr, reg);
		break;
	case OPCODE_IF:
		if (reg) {
			ins_ptr = op1;
		}
		break;
	case OPCODE_RUN:
		debug_mode = 0;
		run_mode = 1;
		goto OPCODE_CALL;
	case OPCODE_DBG:
		run_mode = 1;
		debug_mode = 1;
		goto OPCODE_CALL;
	case OPCODE_CALL:
		if (stack_used < STACK_SIZE) {
			stack[stack_used] = ins_ptr;
			stack_used++;
			ins_ptr = op1;
		} else {
			/* TODO */
		}
		break;
	case OPCODE_RET:
		if (stack_used > 0) {
			stack_used--;
			ins_ptr = stack[stack_used];
		} else {
			/* TODO */
		}
		break;
	}
	if (debug_mode) {
		memset(payload, 0, RPMSG_BUF_SIZE);
		payload[0] = NIB2ASC((ins_ptr >> 4)&0xF);
		payload[1] = NIB2ASC(ins_ptr&0xF);
		payload[2] = ':';
		payload[3] = NIB2ASC((ins >> 28)&0xF);
		payload[4] = NIB2ASC((ins >> 24)&0xF);
		payload[5] = NIB2ASC((ins >> 20)&0xF);
		payload[6] = NIB2ASC((ins >> 16)&0xF);
		payload[7] = NIB2ASC((ins >> 12)&0xF);
		payload[8] = NIB2ASC((ins >> 8)&0xF);
		payload[9] = NIB2ASC((ins >> 4)&0xF);
		payload[10] = NIB2ASC((ins)&0xF);
		payload[11] = ' ';
		payload[12] = NIB2ASC((reg >> 28)&0xF);
		payload[13] = NIB2ASC((reg >> 24)&0xF);
		payload[14] = NIB2ASC((reg >> 20)&0xF);
		payload[15] = NIB2ASC((reg >> 16)&0xF);
		payload[16] = NIB2ASC((reg >> 12)&0xF);
		payload[17] = NIB2ASC((reg >> 8)&0xF);
		payload[18] = NIB2ASC((reg >> 4)&0xF);
		payload[19] = NIB2ASC((reg)&0xF);
		pru_rpmsg_send(&transport, dst, src, payload, 20);
	}
}

void update_timers() {
	
}

int32_t opfetch(uint32_t optype, uint32_t opaddr) {
	int32_t op = 0;
	switch (optype) {
	default:
		break;
	case REG_VARIABLE:
		if (opaddr > data_used) {
			/* TODO */
		}
		op = data[opaddr];
		break;
	case REG_DIO:
		op = (__R31 >> opaddr) & 1;
		break;
	case REG_AO:
	case REG_AI:
	case REG_TMR:
	case REG_PWM:
	case REG_SERVO:
		/* TODO */
		op = 0xFFFFFFFF;
		break;
	case REG_VER:
		op = VERSION;
		break;
	case REG_IMMEDIATE:
		op = (int32_t)((opaddr&0x80)?(opaddr|0xFFFFFF00):opaddr);
		break;
	}

	return op;
}

void opstore(uint32_t optype, uint32_t opaddr, int32_t op) {
}

// Sets pinmux
#pragma DATA_SECTION(init_pins, ".init_pins")
#pragma RETAIN(init_pins)
const char init_pins[] =
	"\0\0";
