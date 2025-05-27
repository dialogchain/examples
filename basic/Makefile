# Makefile for DialogChain Basic Examples

# Configuration
PYTHON = python3.11
# Use the full path to the Python executable
PYTHON_PATH := $(shell which python3)
# Set PYTHONPATH to include the dialogchain source
DC_CMD = PYTHONPATH=../../python $(PYTHON) -m dialogchain.cli
CONFIG_DIR = .
INPUT_DIR = input
OUTPUT_DIR = output
LOG_DIR = logs

# Colors
GREEN = \033[0;32m
NC = \033[0m

# Help
help:
	@echo "\n${GREEN}DialogChain Basic Examples${NC}\n"
	@echo "Available targets:"
	@echo "  make help             - Show this help message"
	@echo "  make deps             - Install required dependencies"
	@echo "  make setup            - Create required directories"
	@echo "  make clean            - Clean up generated files"
	@echo "  make test             - Run all tests"
	@echo ""
	@echo "Examples:"
	@echo "  make timer-to-log     - Run timer to log example"
	@echo "  make http-handler     - Run HTTP handler example"
	@echo "  make file-watcher     - Run file watcher example"

# Dependencies
deps:
	@echo "\n${GREEN}Installing dependencies...${NC}"
	# Install minimal dependencies for basic examples
	pip install -e .
	# Install dialogchain in development mode without dependencies
	cd ../../python && pip install -e . --no-deps && cd -
	# Install any additional requirements
	pip install aiohttp python-dotenv pyyaml

# Setup
dirs:
	@echo "\n${GREEN}Creating directories...${NC}"
	mkdir -p $(INPUT_DIR) $(OUTPUT_DIR) $(LOG_DIR)

# Clean
clean:
	@echo "\n${GREEN}Cleaning up...${NC}"
	rm -rf $(OUTPUT_DIR)/* $(LOG_DIR)/* __pycache__/ .pytest_cache/ .coverage htmlcov/

# Tests
test: deps
	@echo "\n${GREEN}Running tests...${NC}"
	pytest -v

# Set the PYTHONPATH to include the dialogchain source directory
export PYTHONPATH := ../../python/src:$(PYTHONPATH)

# Examples
timer-to-log: dirs
	@echo "\n${GREEN}Running Timer to Log example...${NC}"
	cd ../../python && $(PYTHON) -m dialogchain.cli run --config ../examples/basic/timer_to_log.yaml

http-handler: dirs
	@echo "\n${GREEN}Running HTTP Handler example...${NC}"
	@echo "Send a request: curl http://localhost:8080/hello"
	cd ../../python && $(PYTHON) -m dialogchain.cli run --config ../examples/basic/http_handler.yaml

file-watcher: dirs
	@echo "\n${GREEN}Running File Watcher example...${NC}"
	@echo "Create files in the $(INPUT_DIR) directory to see them processed"
	cd ../../python && $(PYTHON) -m dialogchain.cli run --config ../examples/basic/file_watcher.yaml

# Alias for setup
setup: deps dirs

.PHONY: help deps setup clean test timer-to-log http-handler file-watcher
