////////////////////////////////////////
//	bitflip.arm.c
//	Demo of shared memory
//	Usage:	This takes the first word of SHARED_RAM and flips every other bit
//				over and over.
//          If /dev/uio0 doesn't exist, consider using
//              sudo ./bitflip.arm.out /dev/mem 0x4a300000
//	Wiring:	None
//	Setup:	Run this on the ARM and run bitflip.pru0.c or bitflip.pru1.c on the PRU
//	See:	 
//	PRU:	
////////////////////////////////////////
#include <stdio.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <unistd.h>
#include <stdlib.h>
#include <string.h>
#include <sys/mman.h>

#define PRUSS_SHARED_RAM_OFFSET		0x10000

int main(int argc, const char** argv) {
	unsigned int i, j, mem_dev;
	off_t offset = 0;
	char * driver = "/dev/uio0";

	/* Open shared memory driver */
	if(argc>1)
	    driver = strdup(argv[1]);

	/* Use specified offset */
	if(argc>2)
		offset = (off_t)strtol(argv[2],0,0);

	/* Allocate shared memory pointer to PRU0 DATARAM */
	printf("Opening %s offset 0x%08x\n", driver, offset);
	mem_dev = open(driver, O_RDWR | O_SYNC);
	volatile int *shared_dataram = mmap(NULL,
		16+PRUSS_SHARED_RAM_OFFSET,	/* grab 16 bytes of shared dataram, must allocate with offset of 0 */
		PROT_READ | PROT_WRITE,
		MAP_SHARED,
		mem_dev,
		offset		/* offset must be 0 for /dev/uio0 */
	);
	if(!shared_dataram) {
		
	}
	shared_dataram += (PRUSS_SHARED_RAM_OFFSET/4);

	printf("shared_dataram = %p\n", shared_dataram);
	j = *shared_dataram;
	printf("Read 0x%08x\n", j);

	for(i=0; i<10; i++) {
		printf("Writing 0x%08x\n", i);
		*shared_dataram = i;
		usleep(1);
		j = *shared_dataram;
		printf("Read 0x%08x (%s, Mask=0x%08x)\n", j, j==i?"not flipped":"flipped!", j^i);
	}
	
	return(0);
}
