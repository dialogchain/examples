# Makefile for DialogChain Basic Examples

# Configuration
PYTHON = python3
DC_CMD = cd ../../python && $(PYTHON) -m dialogchain.cli
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
	pip install -e ../../python
	pip install aiohttp python-dotenv

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

# Examples
timer-to-log: dirs
	@echo "\n${GREEN}Running Timer to Log example...${NC}"
	$(DC_CMD) run --config $(CONFIG_DIR)/timer_to_log.yaml

http-handler: dirs
	@echo "\n${GREEN}Running HTTP Handler example...${NC}"
	@echo "Send a request: curl http://localhost:8080/hello"
	$(DC_CMD) run --config $(CONFIG_DIR)/http_handler.yaml

file-watcher: dirs
	@echo "\n${GREEN}Running File Watcher example...${NC}"
	@echo "Create files in the $(INPUT_DIR) directory to see them processed"
	$(DC_MD) run --config $(CONFIG_DIR)/file_watcher.yaml

# Alias for setup
setup: deps dirs

.PHONY: help deps setup clean test timer-to-log http-handler file-watcher
