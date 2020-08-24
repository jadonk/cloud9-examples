// //////////////////////////////////////
// 	toggle1.c
//  Toggles the P9_14 pin as fast as it can. P9_14 is line 18 on chip 1.
// 	Wiring:	Attach an oscilloscope to P9_14 to see the squarewave or 
//          uncomment the usleep and attach an LED.
// 	Setup:	sudo apt uupdate; sudo apt install libgpiod-dev
// 	See:	https://github.com/starnight/libgpiod-example/blob/master/libgpiod-led/main.c
// //////////////////////////////////////
#include <gpiod.h>
#include <stdio.h>
#include <unistd.h>

#define	CONSUMER	"Consumer"

int main(int argc, char **argv)
{
	int chipnumber = 1;
	unsigned int line_num = 18;	// GPIO Pin P9_14
	unsigned int val;
	struct gpiod_chip *chip;
	struct gpiod_line *line;
	int i, ret;

	chip = gpiod_chip_open_by_number(chipnumber);
	if (!chip) {
		perror("Open chip failed\n");
		goto end;
	}

	line = gpiod_chip_get_line(chip, line_num);
	if (!line) {
		perror("Get line failed\n");
		goto close_chip;
	}

	ret = gpiod_line_request_output(line, CONSUMER, 0);
	if (ret < 0) {
		perror("Request line as output failed\n");
		goto release_line;
	}

	/* Blink */
	val = 0;
	while(1) {
		ret = gpiod_line_set_value(line, val);
		if (ret < 0) {
			perror("Set line output failed\n");
			goto release_line;
		}
		// printf("Output %u on line #%u\n", val, line_num);
		// usleep(100000);		// Number of microseconds to sleep
		val = !val;
	}

release_line:
	gpiod_line_release(line);
close_chip:
	gpiod_chip_close(chip);
end:
	return 0;
}
