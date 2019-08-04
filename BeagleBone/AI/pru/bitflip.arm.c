#include <stdio.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <unistd.h>
#include <stdlib.h>
#include <sys/mman.h>

#define PRUSS_SHARED_RAM_OFFSET		0x10000

void main(int argc, const char** argv) {
	unsigned int i, j, mem_dev;

	/* Allocate shared memory pointer to PRU0 DATARAM */
	if(argc==2)
		mem_dev = open(argv[1], O_RDWR | O_SYNC);
	else
		mem_dev = open("/dev/uio0", O_RDWR | O_SYNC);
	volatile int *shared_dataram = mmap(NULL,
		16+PRUSS_SHARED_RAM_OFFSET,	/* grab 16 bytes of shared dataram, must allocate with offset of 0 */
		PROT_READ | PROT_WRITE,
		MAP_SHARED,
		mem_dev,
		0
	);
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
}
