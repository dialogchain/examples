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


# Installation
install:
	pip install -e .
	pip install python-nmap opencv-python pycups
	@echo "✅ DialogChain installed"

venv:
	python3 -m venv venv
	source venv/bin/activate
	@echo "✅ Virtual environment created"

dev: install
	pip install -e ".[dev]"
	@echo "✅ Development environment ready"

# Dependencies for different languages
install-deps:
	@echo "Installing dependencies for external processors..."
	# Python NLP dependencies
	pip install transformers spacy nltk

	# Check if Go is installed (optional)
	@which go > /dev/null && echo "✅ Go found: $$(go version)" || echo "ℹ️  Go not found. Install from https://golang.org/dl/ if needed"

	# Check if Node.js is installed (optional)
	@which node > /dev/null && echo "✅ Node.js found: $$(node --version)" || echo "ℹ️  Node.js not found. Install from https://nodejs.org/ if needed"

	# Check if Rust is installed
	@which cargo > /dev/null || (echo "⚠️  Rust not found. Install from https://rustup.rs/")
	@which cargo > /dev/null && echo "✅ Rust found: $$(cargo --version)"

# Development
test: venv test-unit test-integration test-e2e

# Run unit tests
test-unit:
	@pytest tests/unit/ -v --cov=src/dialogchain --cov-report=term-missing
	@echo "✅ Unit tests completed"

# Run integration tests
test-integration:
	@pytest tests/integration/ -v --cov=src/dialogchain --cov-append
	@echo "✅ Integration tests completed"

# Run end-to-end tests
test-e2e:
	@pytest tests/e2e/ -v --cov=src/dialogchain --cov-append
	@echo "✅ End-to-end tests completed"

# Run tests with coverage report
coverage:
	@coverage erase
	@coverage run -m pytest
	@coverage report -m
	@coverage html
	@echo "📊 Coverage report available at htmlcov/index.html"

# Run type checking
typecheck:
	@mypy src/dialogchain/
	@echo "✅ Type checking completed"

# Run all linters
lint:
	@echo "🔍 Running flake8..."
	@flake8 src/dialogchain/ tests/
	@echo "🎨 Checking code formatting with black..."
	@black --check src/dialogchain/ tests/
	@echo "📝 Checking import ordering..."
	@isort --check-only --profile black src/dialogchain/ tests/
	@echo "✅ Linting completed"

# Format code
format:
	@echo "🎨 Formatting code with black..."
	@black src/dialogchain/ tests/
	@echo "📝 Sorting imports..."
	@isort --profile black src/dialogchain/ tests/
	@echo "✅ Code formatted"

# Check code style without making changes
check-codestyle:
	@black --check --diff src/dialogchain/ tests/
	@isort --check-only --profile black src/dialogchain/ tests/


# Run all checks (lint, typecheck, test)
check-all: lint typecheck test
	@echo "✨ All checks passed!"

# Install pre-commit hooks
pre-commit-install:
	@pre-commit install
	@pre-commit install --hook-type pre-push
	@echo "✅ Pre-commit hooks installed"

# Setup development environment
setup-dev-env: install pre-commit-install
	@echo "🚀 Development environment ready!"

# Build
clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	find . -name "*.pyc" -delete
	find . -name "__pycache__" -delete
	@echo "✅ Cleaned build artifacts"

build: clean
	poetry build
	@echo "✅ Distribution packages built"

# Version management
version:
	@if [ -z "$(PART)" ]; then \
		echo "Error: Please specify version part with PART=patch|minor|major"; \
		exit 1; \
	fi
	@echo "Bumping $$(poetry version $(PART) --dry-run) → $$(poetry version $(PART))"
	git add pyproject.toml
	git commit -m "Bump version to $$(poetry version --short)"
	git tag -a "v$$(poetry version --short)" -m "Version $$(poetry version --short)"
	@echo "✅ Version bumped and tagged. Don't forget to push with tags: git push --follow-tags"

# View recent logs from the application
LINES ?= 50  # Default number of lines to show
LOG_DIR ?= logs  # Default log directory

logs:
	@echo "📋 Showing last $(LINES) lines of logs from $(LOG_DIR)/"
	@if [ -d "$(LOG_DIR)" ]; then \
		find "$(LOG_DIR)" -type f -name "*.log" -exec sh -c 'echo "\n📄 {}:"; tail -n $(LINES) {}' \; 2>/dev/null || echo "No log files found in $(LOG_DIR)/"; \
	else \
		echo "Log directory $(LOG_DIR)/ does not exist"; \
	fi

# Helper to get PYPI_TOKEN from files
define get_pypi_token
$(shell \
    if [ -f "${HOME}/.pypirc" ]; then \
        grep -A 2 '\[pypi\]' "${HOME}/.pypirc" 2>/dev/null | grep 'token = ' | cut -d' ' -f3; \
    elif [ -f ".pypirc" ]; then \
        grep -A 2 '\[pypi\]' ".pypirc" 2>/dev/null | grep 'token = ' | cut -d' ' -f3; \
    elif [ -f ".env" ]; then \
        grep '^PYPI_TOKEN=' ".env" 2>/dev/null | cut -d'=' -f2-; \
    fi
)
endef

# Export the function to be used in the recipe
PYPI_TOKEN_FROM_FILE := $(call get_pypi_token)

# Publishing
publish: venv
	@echo "🔄 Bumping version..."
	poetry version patch
	@echo "🧹 Cleaning build artifacts..."
	@$(MAKE) clean
	@echo "🏗️  Building package..."
	poetry build
	@echo "🚀 Publishing to PyPI..."
	poetry publish
	@echo "✅ Successfully published to PyPI"

# Test publishing
TEST_PYPI_TOKEN ?= $(PYPI_TEST_TOKEN)
testpublish: build
	@if [ -z "$(TEST_PYPI_TOKEN)" ]; then \
		echo "Error: Please set PYPI_TEST_TOKEN environment variable"; \
		exit 1; \
	fi
	@echo "🚀 Publishing to TestPyPI..."
	poetry publish --build --repository testpypi --username=__token__ --password=$(TEST_PYPI_TOKEN)
	@echo "✅ Successfully published to TestPyPI"

# Try to read PyPI token from common locations
PYPI_TOKEN_FILE ?= $(shell if [ -f "${HOME}/.pypirc" ]; then echo "${HOME}/.pypirc"; elif [ -f ".pypirc" ]; then echo ".pypirc"; elif [ -f ".env" ]; then echo ".env"; fi)

# Extract PyPI token from file if not provided
ifdef PYPI_TOKEN_FILE
    ifeq ("$(PYPI_TOKEN)","")
        PYPI_TOKEN := $(shell if [ -f "$(PYPI_TOKEN_FILE)" ]; then \
            if [ "$(PYPI_TOKEN_FILE)" = "${HOME}/.pypirc" ] || [ "$(PYPI_TOKEN_FILE)" = ".pypirc" ]; then \
                grep -A 2 '\[pypi\]' "$(PYPI_TOKEN_FILE)" 2>/dev/null | grep 'token = ' | cut -d' ' -f3; \
            elif [ "$(PYPI_TOKEN_FILE)" = ".env" ]; then \
                grep '^PYPI_TOKEN=' "$(PYPI_TOKEN_FILE)" 2>/dev/null | cut -d'=' -f2-; \
            fi \
        fi)
    endif
endif

# Release a new patch version and publish
release-patch:
	@echo "🚀 Starting release process..."
	@# Bump patch version
	@echo "🔄 Bumping patch version..."
	@$(MAKE) version PART=patch
	@# Push changes and tags
	@echo "📤 Pushing changes to remote..."
	@git push --follow-tags
	@# Publish to PyPI
	@if [ -n "$(PYPI_TOKEN)" ]; then \
		echo "🔑 Found PyPI token in $(PYPI_TOKEN_FILE)"; \
		echo "🚀 Publishing to PyPI..."; \
		$(MAKE) publish; \
	else \
		echo "ℹ️  PyPI token not found. Tried: ~/.pypirc, .pypirc, .env"; \
		echo "   To publish to PyPI, either:"; \
		echo "   1. Add token to ~/.pypirc or .pypirc: [pypi]\n   token = pypi_..."; \
		echo "   2. Add PYPI_TOKEN=... to .env file"; \
		echo "   3. Run: make release-patch PYPI_TOKEN=your_token_here"; \
	fi
	@echo "✅ Release process completed!"
