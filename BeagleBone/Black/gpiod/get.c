// //////////////////////////////////////
// 	get.c
//  Get the value of P8_13. P8_13 is line 23 on chip 0.
// 	Wiring:	Attach a switch to P8_13 and 3.3V
// 	Setup:	sudo apt uupdate; sudo apt install libgpiod-dev
// 	See:	https://github.com/starnight/libgpiod-example/blob/master/libgpiod-led/main.c
// //////////////////////////////////////
#include <gpiod.h>
#include <stdio.h>
#include <unistd.h>

#define	CONSUMER	"Consumer"

int main(int argc, char **argv)
{
	int chipnumber = 0;
	unsigned int line_num = 23;	// GPIO Pin P8_13
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

	ret = gpiod_line_request_input(line, CONSUMER);
	if (ret < 0) {
		perror("Request line as output failed\n");
		goto release_line;
	}

	/* Get */
	while(1) {
		printf("%d\r", gpiod_line_get_value(line));
		usleep(1000);
	}

release_line:
	gpiod_line_release(line);
close_chip:
	gpiod_chip_close(chip);
end:
	return 0;
}
