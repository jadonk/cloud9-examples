#
# Optional definitions
#
# TARGET - executable to create (currently supports single .c source)
#          should have .<proc>(<n>) extension (lower case, check below for valid options)
#          without TARGET, as of now, we don't have any build targets
#          TODO: work with a list of targets, rather than a single file

#
# Directories (external pacakges, etc.)
#
# COMMON points to where this primary Makefile and shell scripts live.
# PRU_CGT points to the TI PRU compiler directory.
# PRU_SUPPORT points to pru-software-support-package.
# C6X_CGT points to the TI C6X compiler directory.
# GEN_DIR points to where to build the binaries.
COMMON:=$(abspath $(lastword $(MAKEFILE_LIST)/..))
PRU_CGT:=/usr/share/ti/cgt-pru
PRU_SUPPORT:=/usr/lib/ti/pru-software-support-package
C6X_CGT:=/usr/share/ti/cgt-c6x
GEN_DIR=/tmp/cloud9-examples
$(warning COMMON=$(COMMON))

#
# Define PROC and build variables
#
# Arguments:
#   $@ - target name
#
# Variables needed:
#   COMMON - where to find support files
#   PRU_SUPPORT - PRU support package files
#   MODEL - board model (BeagleBoard.org_BeagleBone_AI, TI_AM335x_BeagleBone_Blue, etc.)
#   CHIP - target system-on-chip (am57xx, am335x)
#   CHIP_REV - target system-on-chip with rev (am572x_2_0, am335x)
#   PRUN - identifier for target PRU core
#
# Check which model
define target-to-proc =
ifeq ($(MODEL),BeagleBoard.org_BeagleBone_AI)
CHIP=am57xx
CHIP_REV=am572x_2_0
ifeq ($(suffix $(basename $(1))),.pru1_0)
PRU_DIR=/sys/class/remoteproc/remoteproc0
PRUN=1_0
else ifeq ($(suffix $(basename $(1))),.pru1_1)
PRU_DIR=/sys/class/remoteproc/remoteproc1
PRUN=1_1
else ifeq ($(suffix $(basename $(1))),.pru2_0)
PRU_DIR=/sys/class/remoteproc/remoteproc2
PRUN=2_0
else ifeq ($(suffix $(basename $(1))),.pru2_1)
PRU_DIR=/sys/class/remoteproc/remoteproc3
PRUN=2_1
endif
else
CHIP=am335x
CHIP_REV=am335x
ifeq ($(suffix $(basename $(1))),.pru0)
PRU_DIR=/sys/class/remoteproc/remoteproc1
PRUN=0
else ifeq ($(suffix $(basename $(1))),.pru1)
PRU_DIR=/sys/class/remoteproc/remoteproc2
PRUN=1
endif
endif
ifeq ($(findstring pru,$(suffix $(basename $(1)))),pru)
PROC=PRU
else
PROC=ARM
endif
endef

# Call linker
#
# Arguments:
#   1 - target name
#   2 - sources
define call-linker =
$(warning PROC=$(PROC))
ifeq ($(PROC),PRU)
LD=lnkpru
LINKER_COMMAND_FILE=$(COMMON)/$(CHIP)_$(PROC).cmd
LIBS=--library=$(PRU_SUPPORT)/lib/rpmsg_lib.lib
LDFLAGS=--reread_libs --warn_sections --stack_size=0x100 --heap_size=0x100 -m $(basename $(1)).map \
  -i$(PRU_CGT)/lib -i$(PRU_CGT)/include $(2) $(LINKER_COMMAND_FILE) --library=libc.a $(LIBS)
T=-o $(1)
S=$(2)
else ifeq ($(PROC),ARM)
LD=ld
LDFLAGS=-lc -lm
T=-o $(1)
S=$(2)
endif
endef

# Call compiler
#
# Arguments:
#   1 - target name
#   2 - sources
define call-compiler =
$(warning PROC=$(PROC))
ifeq ($(PROC),PRU)
CC=clpru
CFLAGS=--include_path=$(PRU_SUPPORT)/include --include_path=$(PRU_SUPPORT)/include/$(CHIP_REV) \
  --include_path=$(PRU_CGT)/include $(INCLUDE) -DCHIP=$(CHIP) -DCHIP_IS_$(CHIP) -DMODEL=$(MODEL) -DPROC=$(PROC) -DPRUN=$(PRUN) \
  -v3 -O2 --printf_support=minimal --display_error_number --endian=little --hardware_mac=on \
  --obj_directory=$(GEN_DIR) --pp_directory=$(GEN_DIR) --asm_directory=$(GEN_DIR) -ppd -ppa --asm_listing \
  --c_src_interlist # --absolute_listing
T=-fe $(1)
S=$(2)
else ifeq ($(PROC),ARM)
CC=gcc
CFLAGS=-DCHIP=$(CHIP) -DMODEL=$(MODEL) -DPROC=$(PROC)
T=-o $(1)
S=-c $(2)
endif
endef

#
#
#
MODEL:=$(shell cat /proc/device-tree/model | sed 's/ /_/g' | tr -d '\000')
$(warning MODEL=$(MODEL),TARGET=$(TARGET))

%.out: $(GEN_DIR)/%.out
	@echo 'CP	$^'
	@cp $^ $@

$(GEN_DIR)/%.out: $(GEN_DIR)/%.o
	@echo 'LD	$^'
	$(eval $(call target-to-proc,$@)) $(eval $(call call-linker,$@,$^)) $(LD) $(LDFLAGS) $(T) $(S)

$(GEN_DIR)/%.o: %.c
	@echo 'CC	$^'
	$(eval $(call target-to-proc,$@)) $(eval $(call call-compiler,$@,$^)) $(CC) $(CFLAGS) $(T) $(S)

ifneq ($(TARGET),)
$(eval $(call target-to-proc,$(TARGET).out))
$(warning GEN_DIR=$(GEN_DIR),CHIP=$(CHIP),PROC=$(PROC),PRUN=$(PRUN),PRU_DIR=$(PRU_DIR))

#all: stop install start
all: stop install start
	@echo "MODEL   = $(MODEL)"
	@echo "PROC    = $(PROC)"
	@echo "PRUN    = $(PRUN)"
	@echo "PRU_DIR = $(PRU_DIR)"

stop:
	@echo "-    Stopping PRU $(PRUN)"
	@echo stop | tee $(PRU_DIR)/state || echo Cannot stop $(PRUN)

start:
	@echo "-    Starting PRU $(PRUN)"
	@echo start | tee $(PRU_DIR)/state
	@echo write_init_pins.sh
	@$(COMMON)/write_init_pins.sh /lib/firmware/$(CHIP)-pru$(PRUN)-fw

install: $(GEN_DIR)/$(TARGET).out
	@echo '-	copying firmware file $(GEN_DIR)/$(TARGET).out to /lib/firmware/$(CHIP)-pru$(PRUN)-fw'
	@cp $(GEN_DIR)/$(TARGET).out /lib/firmware/$(CHIP)-pru$(PRUN)-fw

$(GEN_DIR)/$(TARGET).out: $(GEN_DIR)/$(TARGET).o
	@echo 'LD	$^'
	$(eval $(call call-linker,$@,$^))

$(GEN_DIR)/$(TARGET).o: $(TARGET).c
	@mkdir -p $(GEN_DIR)
	@echo 'CC	$<'
	$(warning <=$<,^=$^)
	$(eval $(call call-compiler,$<,$^))

clean:
	@echo 'CLEAN	.    PRU $(PRUN)'
	@rm -rf $(GEN_DIR)
endif
