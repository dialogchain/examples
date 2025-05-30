# DialogChain Examples Makefile
# Manages example configurations and their execution

.PHONY: help list-examples run-example stop-example view-logs \
        clean clean-all setup-env check-deps install-deps

# Default target
help:
	@echo "DialogChain Examples Manager"
	@echo ""
	@echo "Available commands:"
	@echo "  list-examples    - List all available examples"
	@echo "  run-example      - Run a specific example (use EXAMPLE=path/to/example)"
	@echo "  stop-example     - Stop a running example"
	@echo "  view-logs        - View logs for running example"
	@echo "  setup-env        - Create .env file from example"
	@echo "  clean            - Clean temporary files"
	@echo "  clean-all        - Remove all build artifacts and containers"
	@echo "  check-deps       - Check for required dependencies"
	@echo "  install-deps     - Install required dependencies"
	@echo ""
	@echo "Example-specific commands:"
	@echo "  simple-logging   - Run simple logging example"
	@echo "  simple-timer     - Run simple timer example"
	@echo "  file-watcher     - Run file watcher example"
	@echo "  mqtt-example     - Run MQTT example"
	@echo "  http-example     - Run HTTP example"
	@echo "  camera-example   - Run camera example"
	@echo "  iot-example      - Run IoT example"
	@echo "  grpc-example     - Run gRPC example"

# Variables
EXAMPLES_DIR := $(shell pwd)
DOCKER_COMPOSE := docker-compose -f docker-compose.yml
EXAMPLE_PATH ?=

# Find all YAML example files
EXAMPLE_FILES := $(shell find . -type f -name '*.yaml' -o -name '*.yml' | sort | grep -v 'node_modules\|venv\|\.git')

# Docker container name for the example
CONTAINER_NAME := dialogchain-example-$(shell echo $(EXAMPLE_PATH) | tr '/' '-' | tr -d '.')

# Default target
.DEFAULT_GOAL := help

# List all available examples
list-examples:
	@echo "Available examples:"
	@echo "------------------"
	@for example in $(EXAMPLE_FILES); do \
		echo "- $$example"; \
	done

# Run a specific example
run-example: install-deps
	@if [ -z "$(EXAMPLE_PATH)" ]; then \
		echo "Error: Please specify an example with EXAMPLE=path/to/example"; \
		echo "Run 'make list-examples' to see available examples"; \
		echo "Or use one of the example-specific commands like 'make simple-timer'"; \
		exit 1; \
	fi
	@if [ ! -f "$(EXAMPLE_PATH)" ]; then \
		echo "Error: Example file '$(EXAMPLE_PATH)' not found"; \
		exit 1; \
	fi
	@echo "🚀 Starting $(EXAMPLE_PATH) example..."
	@dialogchain run $(EXAMPLE_PATH)

# Install dependencies
install-deps:
	@echo "Installing core dependencies..."
	pip install aiofiles aiohttp asyncio-mqtt python-dotenv click pyyaml grpcio grpcio-tools jinja2 opencv-python numpy python-nmap
	@echo "Installing development dependencies..."
	pip install pytest pytest-asyncio pytest-cov pytest-mock pytest-aiohttp pytest-xdist
	@echo "Installing dependencies for external processors..."
	pip install transformers spacy nltk
	@echo "Adding Python path to PYTHONPATH..."
	@export PYTHONPATH="/home/tom/github/dialogchain/python/src:${PYTHONPATH}"

# Check for required dependencies
check-deps:
	@echo "Checking for required dependencies..."
	@command -v dialogchain >/dev/null 2>&1 || { \
		echo "Error: 'dialogchain' command not found. Please install the package first."; \
		echo "Run 'pip install -e /path/to/dialogchain/python' to install in development mode."; \
		exit 1; \
	}

# Example-specific targets
simple-logging: install-deps
	@echo "🚀 Starting simple logging example..."
	@PYTHONPATH="/home/tom/github/dialogchain/python/src:${PYTHONPATH}" dialogchain run --config ./simple_logging_example.yaml

simple-timer: install-deps
	@echo "⏱️  Starting simple timer example..."
	@PYTHONPATH="/home/tom/github/dialogchain/python/src:${PYTHONPATH}" dialogchain run --config ./simple_timer_example.yaml

file-watcher: install-deps
	@echo "👁️  Starting file watcher example..."
	@PYTHONPATH="/home/tom/github/dialogchain/python/src:${PYTHONPATH}" dialogchain run --config ./file_watcher_example.yaml

mqtt-example: install-deps
	@echo "📡 Starting MQTT example..."
	@PYTHONPATH="/home/tom/github/dialogchain/python/src:${PYTHONPATH}" dialogchain run --config ./integrations/mqtt/mqtt_example.yaml

http-example: install-deps
	@echo "🌐 Starting HTTP example..."
	@PYTHONPATH="/home/tom/github/dialogchain/python/src:${PYTHONPATH}" dialogchain run --config ./integrations/http/http_timer_example.yaml

camera-example: install-deps
	@echo "📷 Starting camera example..."
	@PYTHONPATH="/home/tom/github/dialogchain/python/src:${PYTHONPATH}" dialogchain run --config ./advanced/camera/camera_routes.yaml

iot-example: install-deps
	@echo "🏠 Starting IoT example..."
	@PYTHONPATH="/home/tom/github/dialogchain/python/src:${PYTHONPATH}" dialogchain run --config ./advanced/iot/iot_routes.yaml

grpc-example: install-deps
	@echo "🔌 Starting gRPC example..."
	@PYTHONPATH="/home/tom/github/dialogchain/python/src:${PYTHONPATH}" dialogchain run --config ./integrations/grpc/grpc_routes.yaml

# Cleanup targets
clean:
	@echo "Cleaning temporary files..."
	@rm -f *.log *.tmp

clean-all: clean
	@echo "Removing build artifacts and containers..."
	@docker-compose down -v --remove-orphans

# Setup environment
setup-env:
	@if [ ! -f .env ]; then \
		echo "# DialogChain Example Environment Variables" > .env; \
		echo "# Add your environment variables here" >> .env; \
		echo "" >> .env; \
	fi

# View logs
view-logs:
	@if [ -z "$(CONTAINER_NAME)" ]; then \
		echo "Error: No container name specified"; \
		exit 1; \
	fi
	@docker logs -f $(CONTAINER_NAME)

# Stop a running example
stop-example:
	@if [ -z "$(CONTAINER_NAME)" ]; then \
		echo "Error: No container name specified"; \
		exit 1; \
	fi
	@docker stop $(CONTAINER_NAME) 2>/dev/null || echo "No running container found with name $(CONTAINER_NAME)"
