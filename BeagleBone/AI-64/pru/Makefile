all: blinkR30.j7-pru0_0.out ring.j7-pru0_0.out
	@echo "Built!"

blinkR30:
	make -f /var/lib/cloud9/common/Makefile TARGET=blinkR30.j7-pru0_0

include /var/lib/cloud9/common/Makefile

clean:
	rm -f *.out
	rm -rf $(GEN_DIR)

