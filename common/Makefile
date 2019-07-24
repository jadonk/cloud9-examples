#
# Directories (external pacakges, etc.)
#
# COMMON points to where this primary Makefile and shell scripts live.
# PRU_CGT points to the TI PRU compiler directory.
# PRU_SUPPORT points to pru-software-support-package.
# PRU_CGT points to the TI PRU compiler directory.
# GEN_DIR points to where to put the generated files.

COMMON:=$(abspath $(lastword $(MAKEFILE_LIST)))
PRU_CGT:=/usr/share/ti/cgt-pru
PRU_SUPPORT:=/usr/lib/ti/pru-software-support-package
C6X_CGT:=/usr/share/ti/cgt-c6x
GEN_DIR:=.

#
#
#
MODEL:=$(shell cat /proc/device-tree/model | sed 's/ /_/g' | tr -d '\000')
$(warning MODEL=$(MODEL))

.c.out:
	echo "got here: $< $(suffix $(basename $<))"
	$(eval $(call target-to-proc,$<))
	$(warning CHIP=$(CHIP),PROC=$(PROC),PRUN=$(PRUN),PRU_DIR=$(PRU_DIR))

#
# PRU defines
#
# Let's refer to a cmd file in /usr/lib/ti/pru-support-package instead I think
PRU_LINKER_COMMAND_FILE=AM57xx_PRU.cmd
PRU_LIBS=--library=$(PRU_SUPPORT)/lib/rpmsg_lib.lib
PRU_INCLUDE=--include_path=$(PRU_SUPPORT)/include --include_path=$(PRU_SUPPORT)/include/am335x
PRU_STACK_SIZE=0x100
PRU_HEAP_SIZE=0x100
PRU_CFLAGS=-v3 -O2 --printf_support=minimal --display_error_number --endian=little --hardware_mac=on --obj_directory=$(GEN_DIR) --pp_directory=$(GEN_DIR) --asm_directory=$(GEN_DIR) -ppd -ppa --asm_listing --c_src_interlist -DAI=$(AI) # --absolute_listing
PRU_LFLAGS=--reread_libs --warn_sections --stack_size=$(PRU_STACK_SIZE) --heap_size=$(PRU_HEAP_SIZE) -m $(GEN_DIR)/$(TARGET).map

# Check which model
define target-to-proc =
  PROC=ARM
  ifeq ($(MODEL),BeagleBoard.org_BeagleBone_AI)
    CHIP=am57xx
    ifeq ($(suffix $(basename $(1))),.pru1_0)
      PROC=PRU
      PRUN=1_0
      PRU_DIR=/sys/class/remoteproc/remoteproc0
    endif
    ifeq ($(suffix $(basename $(1))),.pru1_1)
      PROC=PRU
      PRUN=1_1
      PRU_DIR=/sys/class/remoteproc/remoteproc1
    endif
    ifeq ($(suffix $(basename $(1))),.pru2_0)
      PROC=PRU
      PRUN=2_0
      PRU_DIR=/sys/class/remoteproc/remoteproc2
    endif
    ifeq ($(suffix $(basename $(1))),.pru2_1)
      PROC=PRU
      PRUN=2_1
      PRU_DIR=/sys/class/remoteproc/remoteproc3
    endif
  else
    CHIP=am335x
    ifeq ($(suffix $(basename $(1))),.pru0)
      PROC=PRU
      PRUN=0
      PRU_DIR=/sys/class/remoteproc/remoteproc1
    endif
    ifeq ($(suffix $(basename $(1))),.pru1)
      PROC=PRU
      PRUN=1
      PRU_DIR=/sys/class/remoteproc/remoteproc2
    endif
  endif
endef

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

$(GEN_DIR)/$(TARGET).out: $(GEN_DIR)/$(TARGET).obj
	@echo 'LD	$^' 
	@lnkpru -i$(PRU_CGT)/lib -i$(PRU_CGT)/include $(LFLAGS) -o $@ $^ $(LINKER_COMMAND_FILE) --library=libc.a $(LIBS) $^

$(GEN_DIR)/$(TARGET).obj: $(TARGET).c
	@mkdir -p $(GEN_DIR)
	@echo 'CC	$<'
	@clpru --include_path=$(PRU_CGT)/include $(INCLUDE) $(CFLAGS) -D=PRUN=$(PRUN) -fe $@ $<

clean:
	@echo 'CLEAN	.    PRU $(PRUN)'
	@rm -rf $(GEN_DIR)
