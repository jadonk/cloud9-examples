/****************************************************************************/
/*  tda4vm_pru.cmd                                                          */
/*  Copyright (c) 2015  Texas Instruments Incorporated                      */
/*  Copyright (c) 2021 Jason Kridner <jkridner@beagleboard.org>             */
/*                                                                          */
/*    Description: This file is a linker command file that can be used for  */
/*                 linking PRU programs built with the C compiler and       */
/*                 the resulting .out file on an TDA4VM device.             */
/****************************************************************************/

-cr								/* Link using C conventions */

/* Specify the System Memory Map */
MEMORY
{
PAGE 0:
	PRU_IMEM	: org = 0x00000000 len = 0x00003000  /* 12kB Instruction RAM */

PAGE 1:
	PRU_DMEM_0_1	: org = 0x00000000 len = 0x00002000 CREGISTER=24 /* 8kB PRU Data RAM 0_1 */
	PRU_DMEM_1_0	: org = 0x00002000 len = 0x00002000 CREGISTER=25 /* 8kB PRU Data RAM 1_0 */

PAGE 2:
	PRU_SHAREDMEM	: org = 0x00010000 len = 0x00008000 CREGISTER=28 /* 32kB Shared RAM */
}

/* Specify the sections allocation into memory */
SECTIONS {
	/* Forces _c_int00 to the start of PRU IRAM. Not necessary when loading
	   an ELF file, but useful when loading a binary */
	.text:_c_int00*	>  0x0, PAGE 0

	.text		>  PRU_IMEM, PAGE 0
	.stack		>  PRU_DMEM_0_1, PAGE 1
	.bss		>  PRU_DMEM_0_1, PAGE 1
	.cio		>  PRU_DMEM_0_1, PAGE 1
	.data		>  PRU_DMEM_0_1, PAGE 1
	.switch		>  PRU_DMEM_0_1, PAGE 1
	.sysmem		>  PRU_DMEM_0_1, PAGE 1
	.cinit		>  PRU_DMEM_0_1, PAGE 1
	.rodata		>  PRU_DMEM_0_1, PAGE 1
	.rofardata	>  PRU_DMEM_0_1, PAGE 1
	.farbss		>  PRU_DMEM_0_1, PAGE 1
	.fardata	>  PRU_DMEM_0_1, PAGE 1

	.resource_table > PRU_DMEM_0_1, PAGE 1
	.init_pins	> PRU_DMEM_0_1, PAGE 1
}
