// //////////////////////////////////////
// 	getset.c
//  Get the value of P8_16 and write it to P9_14. 
//     P8_16 is line 14 on chip 1.  P9_14 is line 18 of chip 1.
// 	Wiring:	Attach a switch to P8_16 and 3.3V and an LED to P9_14.
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
	unsigned int getline_num = 14;	// GPIO Pin P8_16
	unsigned int setline_num = 18;	// GPIO Pin P9_14
	unsigned int val;
	struct gpiod_chip *chip;
	struct gpiod_line *getline, *setline;
	int i, ret;

	chip = gpiod_chip_open_by_number(chipnumber);
	if (!chip) {
		perror("Open chip failed\n");
		goto end;
	}

	getline = gpiod_chip_get_line(chip, getline_num);
	if (!getline) {
		perror("Get line failed\n");
		goto close_chip;
	}

	setline = gpiod_chip_get_line(chip, setline_num);
	if (!setline) {
		perror("Set line failed\n");
		goto close_chip;
	}

	ret = gpiod_line_request_input(getline, CONSUMER);
	if (ret < 0) {
		perror("Request line as input failed\n");
		goto release_line;
	}

	ret = gpiod_line_request_output(setline, CONSUMER, 0);
	if (ret < 0) {
		perror("Request line as output failed\n");
		goto release_line;
	}

	/* Get */
	while(1) {
		val = gpiod_line_get_value(getline);
		gpiod_line_set_value(setline, val);
		// printf("%d\r", val);
		// usleep(1000);
	}

release_line:
	gpiod_line_release(getline);
	gpiod_line_release(setline);
close_chip:
	gpiod_chip_close(chip);
end:
	return 0;
}
