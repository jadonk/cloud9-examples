#include <stdio.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <unistd.h>
#include <stdlib.h>
#include <sys/mman.h>

#define AM33XX_DATARAM0_PHYS_BASE		0x4a300000
#define AM33XX_DATARAM1_PHYS_BASE		0x4a302000
#define AM33XX_PRUSS_SHAREDRAM_BASE		0x4a310000

void main() {
	unsigned int i, j;

	/* Allocate shared memory pointer to PRU0 DATARAM */
	int mem_dev = open("/dev/mem", O_RDWR | O_SYNC);
	volatile void *shared_dataram = mmap(NULL,
		16,	/* grab 16 bytes */
		PROT_READ | PROT_WRITE,
		MAP_SHARED,
		mem_dev,
		AM33XX_PRUSS_SHAREDRAM_BASE
	);

	printf("shared_dataram = %p\n", shared_dataram);
	j = *(unsigned int *)shared_dataram;
	printf("Read 0x%08x\n", j);

	for(i=0; i<10; i++) {
		printf("Writing 0x%08x\n", i);
		*(unsigned int *)shared_dataram = i;
		usleep(1);
		j = *(unsigned int *)shared_dataram;
		printf("Read 0x%08x (0x%08x)\n", j, j^0xAAAAAAAA);
	}
}
