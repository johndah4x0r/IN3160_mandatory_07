# Makefile

# defaults
SIM ?= ghdl
TOPLEVEL_LANG ?= vhdl

# VHDL 2008
EXTRA_ARGS +=--std=08
COCOTB_HDL_TIMEPRECISION = 1fs

# TOPLEVEL is the name of the toplevel module in your VHDL file
TOPLEVEL = pdm

VHDL_SOURCES += $(PWD)/../src/*.vhd

SIM_ARGS +=--wave=$(TOPLEVEL).ghw 

# COCOTB_TEST_MODULES is the basename of the Python test file
COCOTB_TEST_MODULES = tb_$(TOPLEVEL)

# include cocotb's make rules to take care of the simulator setup
include $(shell cocotb-config --makefiles)/Makefile.sim

# removing generated binaries and python cache when using make clean
clean::
	-@rm -rf __pycache__
	-@rm -rf sim_build
