# Makefile for running a fixed Python script with an optional YAML configuration file

# Define the Python script path
PYTHON_SCRIPT = generator.py

# Current directory from which the Makefile is executed
CALL_DIR := $(PWD)

# Default target
.PHONY: run
run:
ifdef CONFIG
	python3 $(PYTHON_SCRIPT) "$(CALL_DIR)" "$(CONFIG)"
else
	python3 $(PYTHON_SCRIPT) "$(CALL_DIR)"
endif

# Help target to show usage information
.PHONY: help
help:
	@echo "Usage: make run [CONFIG=<path_to_config_file>]"
	@echo "  CONFIG=<path_to_config_file>  Path to a YAML configuration file to be passed to the Python script."
	@echo "  The current directory (where make is called) is also passed to the Python script, and spaces in paths are handled."
