all: bitflip.arm.out bitflip.pru1_1.out blinkExternalLED.pru1_1.out blinkInternalLED.pru1_1.out \
	blinkR30.pru1_1.out inputR31.pru1_1.out neopixelDynamic.pru1_1.out neopixelRpmsg.pru1_1.out \
	neopixelStatic.pru1_1.out # shared.pru1_1.out
	@echo "Built!"

include /var/lib/cloud9/common/Makefile

clean:
	rm -f *.out
	rm -rf $(GEN_DIR)

