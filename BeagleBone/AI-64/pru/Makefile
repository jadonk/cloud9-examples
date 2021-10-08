all: ring.j7-pru0_0.out \
  blinkR30.j7-pru0_0.out \
  blinkR30.j7-pru0_1.out \
  blinkR30.j7-pru1_0.out \
  blinkR30.j7-pru1_1.out
	@echo "Built!"

blinkR30:
	make -f /var/lib/cloud9/common/Makefile TARGET=blinkR30.j7-pru0_0
	make -f /var/lib/cloud9/common/Makefile TARGET=blinkR30.j7-pru0_1
	make -f /var/lib/cloud9/common/Makefile TARGET=blinkR30.j7-pru1_0
	make -f /var/lib/cloud9/common/Makefile TARGET=blinkR30.j7-pru1_1

include /var/lib/cloud9/common/Makefile

clean:
	rm -f *.out
	rm -rf $(GEN_DIR)

