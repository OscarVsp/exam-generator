# Makefile for running a fixed Python script with optional YAML CFGuration file and additional parameters

# Define the Python script path
PYTHON_SCRIPT = generator.py

# Current directory from which the Makefile is executed
CALL_DIR := $(PWD)

# Default target
.PHONY: run
run:
	@if [ -n "$(CONF)" ] || [ -n "$(STUDENTS)" ] || [ -n "$(DS_PATH)" ] || [ -n "$(OUTPUT_PATH)" ]; then \
		if [ -z "$(CONF)" ] || [ -z "$(STUDENTS)" ] || [ -z "$(DS_PATH)" ] || [ -z "$(OUTPUT_PATH)" ]; then \
			$(MAKE) help; \
			exit 1; \
		fi; \
		python3 $(PYTHON_SCRIPT) "$(CALL_DIR)/$(CONF)" "$(CALL_DIR)/$(STUDENTS)" "$(CALL_DIR)/$(DS_PATH)" "$(CALL_DIR)/$(OUTPUT_PATH)"; \
	else \
		python3 $(PYTHON_SCRIPT); \
	fi

# Install dependencies target
.PHONY: install
install:
	apt-get update
	apt-get install -y texlive latexmk texlive-xetex python3-yaml

# Help target to show usage information
.PHONY: help
help:
	@echo "Usage: make run [CONF=<path_to_CFG_file>] [STUDENTS=<path_to_STUDENTS>] [DS_PATH=<path_to_dataset>] [OUTPUT_PATH=<path_to_output_dir>]"
	@echo "  CONF=<path_to_CONF_file>      Path to a YAML CFGuration file to be passed to the Python script."
	@echo "  STUDENTS=<path_to_STUDENTS> Path to the student list file."
	@echo "  DS_PATH=<path_to_dataset>    Path to the dataset directory."
	@echo "  OUTPUT_PATH=<path_to_output_dir>   Path to the output directory."
	@echo "  The directory from which make is called is also passed to the Python script."
	@echo "To install dependencies, run: make install"
