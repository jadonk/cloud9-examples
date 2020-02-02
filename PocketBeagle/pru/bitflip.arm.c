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
#include <errno.h>

#define PRUSS_SHARED_RAM_OFFSET		0x10000

int main(int argc, const char** argv) {
	unsigned int i, j, mem_dev;
	off_t alloc_offset = 0x2000;		/* offset must be 0x2000 for this driver */
	size_t size = 16; 					/* grab 16 bytes of shared dataram */
	char * driver = "/dev/uio/pru-shmem";
	int access_offset = 0;

	/* Open shared memory driver */
	if(argc>1)
	    driver = strdup(argv[1]);

	/* Use specified allocation offset */
	if(argc>2)
		alloc_offset = (off_t)strtol(argv[2],0,0);

	/* Use specified access offset */
	if(argc>3) {
		access_offset = (off_t)strtol(argv[3],0,0);
	}

	/* Use specified size */
	if(argc>4) {
		size = (off_t)strtol(argv[4],0,0);
	}

	/* Allocate shared memory pointer to PRU0 DATARAM */
	size += access_offset; /* In case allocation must have a different offset */
	printf("Opening %s offset 0x%08x and size 0x%08x with access offset 0x%08x\n", 
		driver, alloc_offset, size, access_offset);
	mem_dev = open(driver, O_RDWR | O_SYNC);
	volatile int *shared_dataram = mmap(NULL,
		size,
		PROT_READ | PROT_WRITE,
		MAP_SHARED,
		mem_dev,
		alloc_offset
	);
	if(shared_dataram == MAP_FAILED) {
		perror("mmap");
		exit(-1);
	}
	shared_dataram += (access_offset/4);

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
