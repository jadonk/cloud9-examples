#
# Optional definitions
#
# TARGET - executable to create (currently supports single .c source)
#          should have .<proc>(<n>) extension (lower case, check below for valid options)
#          without TARGET, as of now, we don't have any build targets
#          TODO: work with a list of targets, rather than a single file
# PRUN   - TBD

#
# Directories (external packages, etc.)
#
# COMMON points to where this primary Makefile and shell scripts live.
# PRU_CGT points to the TI PRU compiler directory.
# PRU_SUPPORT points to pru-software-support-package.
# C6X_CGT points to the TI C6X compiler directory.
# GEN_DIR points to where to build the binaries.
# MODEL is the board model (BeagleBoard.org_BeagleBone_AI, TI_AM335x_BeagleBone_Blue, etc.)
COMMON:=$(abspath $(lastword $(MAKEFILE_LIST)/..))
PRU_CGT:=/usr/share/ti/cgt-pru
PRU_SUPPORT:=/usr/lib/ti/pru-software-support-package
C6X_CGT:=/usr/share/ti/cgt-c6x
GEN_DIR:=/tmp/cloud9-examples
MODEL:=$(shell cat /proc/device-tree/model | sed 's/ /_/g' | tr -d '\000')
$(warning MODEL=$(MODEL),TARGET=$(TARGET),COMMON=$(COMMON))

#
# Define PROC and build variables
#
# Arguments:
#   $@ - target name
#
# Variables defined:
#   CHIP - target system-on-chip (am57xx, am335x)
#   CHIP_REV - target system-on-chip with rev (am572x_2_0, am335x)
#   PROC - cpu type (arm, pru, c6x, etc.)
#   PRUN - identifier for target PRU core
#   PRU_DIR - control directory for the PRU
#   CC -
#   LD - 
#   LDFLAGS - 
#   CFLAGS -
#
# Check which model
define target-to-proc =
 ifeq ($(suffix $(basename $(1))),.pru1_0)
  CHIP=am57xx
  CHIP_REV=am572x_2_0
  PRU_DIR=/sys/class/remoteproc/remoteproc0
  PRUN=1_0
 else ifeq ($(suffix $(basename $(1))),.pru1_1)
  CHIP=am57xx
  CHIP_REV=am572x_2_0
  PRU_DIR=/sys/class/remoteproc/remoteproc1
  PRUN=1_1
 else ifeq ($(suffix $(basename $(1))),.pru2_0)
  CHIP=am57xx
  CHIP_REV=am572x_2_0
  PRU_DIR=/sys/class/remoteproc/remoteproc2
  PRUN=2_0
 else ifeq ($(suffix $(basename $(1))),.pru2_1)
  CHIP=am57xx
  CHIP_REV=am572x_2_0
  PRU_DIR=/sys/class/remoteproc/remoteproc3
  PRUN=2_1
 else ifeq ($(suffix $(basename $(1))),.pru0)
  CHIP=am335x
  CHIP_REV=am335x
  PRU_DIR=/sys/class/remoteproc/remoteproc1
  PRUN=0
 else ifeq ($(suffix $(basename $(1))),.pru1)
  CHIP=am335x
  CHIP_REV=am335x
  PRU_DIR=/sys/class/remoteproc/remoteproc2
  PRUN=1
 endif
 ifeq ($(findstring pru,$(suffix $(basename $(1)))),pru)
  PROC=pru
 else
  PROC=arm
 endif
endef

#
# Arguments:
#   $@ - target name
# 
# Variables required:
#   CHIP - target system-on-chip (am57xx, am335x)
#   CHIP_REV - target system-on-chip with rev (am572x_2_0, am335x)
#   PROC - cpu type (arm, pru, c6x, etc.)
#   PRUN - identifier for target PRU core
#   PRU_DIR - control directory for the PRU
define proc-to-build-vars =
 ifeq ($(PROC),pru)
  LD=lnkpru -o
  LDFLAGS=--reread_libs --warn_sections --stack_size=0x100 --heap_size=0x100 -m $(basename $(1)).map \
   -i$(PRU_CGT)/lib -i$(PRU_CGT)/include $(COMMON)/$(CHIP)_$(PROC).cmd --library=libc.a \
   --library=$(PRU_SUPPORT)/lib/rpmsg_lib.lib
  CC=clpru -fe
  CFLAGS=--include_path=$(COMMON) --include_path=$(PRU_SUPPORT)/include \
   --include_path=$(PRU_SUPPORT)/include/$(CHIP_REV) \
   --include_path=$(PRU_CGT)/include -DCHIP=$(CHIP) -DCHIP_IS_$(CHIP) -DMODEL=$(MODEL) -DPROC=$(PROC) -DPRUN=$(PRUN) \
   -v3 -O2 --printf_support=minimal --display_error_number --endian=little --hardware_mac=on \
   --obj_directory=$(GEN_DIR) --pp_directory=$(GEN_DIR) --asm_directory=$(GEN_DIR) -ppd -ppa --asm_listing \
   --c_src_interlist
 else
  LD=gcc -o
  LDFLAGS=-lc -lm
  CC=gcc -c -o
  CFLAGS=-DCHIP=$(CHIP) -DMODEL=$(MODEL) -DPROC=$(PROC)
 endif
endef

#
#
#

ifneq ($(TARGET),)
$(eval $(call target-to-proc,$(TARGET).out))
# $(warning GEN_DIR=$(GEN_DIR),CHIP=$(CHIP),PROC=$(PROC),PRUN=$(PRUN),PRU_DIR=$(PRU_DIR))

all: stop install start
	@echo "MODEL   = $(MODEL)"
	@echo "PROC    = $(PROC)"
	@echo "PRUN    = $(PRUN)"
	@echo "PRU_DIR = $(PRU_DIR)"

# TODO: think about what we want to say if stop fails
stop:
ifneq ($(PRU_DIR),)
	@echo "-    Stopping PRU $(PRUN)"
	@echo stop > $(PRU_DIR)/state || echo Cannot stop $(PRUN)
endif

start:
ifneq ($(PRU_DIR),)
	@echo "-    Starting PRU $(PRUN)"
	@echo start > $(PRU_DIR)/state
	@echo write_init_pins.sh
	@$(COMMON)/write_init_pins.sh /lib/firmware/$(CHIP)-pru$(PRUN)-fw
else
	./$(TARGET).out
endif

install: $(GEN_DIR)/$(TARGET).out
ifneq ($(PRU_DIR),)
	@echo '-	copying firmware file $(GEN_DIR)/$(TARGET).out to /lib/firmware/$(CHIP)-pru$(PRUN)-fw'
	@cp $(GEN_DIR)/$(TARGET).out /lib/firmware/$(CHIP)-pru$(PRUN)-fw
else
	@cp $(GEN_DIR)/$(TARGET).out ./$(TARGET).out
endif
endif

%.out: $(GEN_DIR)/%.out
	@echo 'CP	$^'
	@cp $^ $@

# TODO: look up how Makefiles typically break down the output file specification
# $(warning CHIP=$(CHIP),PROC=$(PROC))
# $(warning CC=$(CC),LD=$(LD),CFLAGS=$(CFLAGS),LDFLAGS=$(LDFLAGS))
$(GEN_DIR)/%.out: $(GEN_DIR)/%.o
	@mkdir -p $(GEN_DIR)
	@echo 'LD	$^'
	$(eval $(call target-to-proc,$@))
	$(eval $(call proc-to-build-vars,$@))
	@$(LD) $@ $^ $(LDFLAGS) 

$(GEN_DIR)/%.o: %.c
	@mkdir -p $(GEN_DIR)
	@echo 'CC	$^'
	$(eval $(call target-to-proc,$@))
	$(eval $(call proc-to-build-vars,$@))
	@$(CC) $@ $^ $(CFLAGS)

clean:
	@echo 'CLEAN'
	@rm -rf $(GEN_DIR)
