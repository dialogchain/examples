# Email Invoices Example Makefile
# Manages the email invoice processing example

.PHONY: help setup install test run clean lint format typecheck \
        run-example stop-example view-logs setup-env

# Project variables
PROJECT_NAME = email-invoice-processor
PYTHON = python3
VENV = .venv
PYTHON_VENV = $(VENV)/bin/python
PIP_VENV = $(VENV)/bin/pip
PYTEST = $(VENV)/bin/pytest
FLAKE8 = $(VENV)/bin/flake8
BLACK = $(VENV)/bin/black
ISORT = $(VENV)/bin/isort
MYPY = $(VENV)/bin/mypy

# Default target
help:
	@echo "\n\033[1m$(PROJECT_NAME) - Makefile Help\033[0m"
	@echo "\nAvailable targets:"
	@echo "  make help         - Show this help message"
	@echo "  make setup        - Set up the development environment"
	@echo "  make install      - Install the package in development mode"
	@echo "  make test         - Run tests"
	@echo "  make lint         - Run code style checks"
	@echo "  make format       - Format the code"
	@echo "  make run          - Run the email processor"
	@echo "  make clean        - Clean up temporary files"

# Setup development environment
setup: venv requirements.txt
	$(PIP_VENV) install -U pip setuptools wheel
	$(PIP_VENV) install -r requirements.txt
	$(PIP_VENV) install -e .

# Create virtual environment
venv:
	if [ ! -d "$(VENV)" ]; then \
		$(PYTHON) -m venv $(VENV) && \
		. $(VENV)/bin/activate && \
		pip install --upgrade pip; \
	fi

# Install the package in development mode
install:
	$(PIP_VENV) install -e .

# Run tests
test:
	$(PYTEST) tests/ -v

# Run code style checks
lint:
	@echo "🔍 Running flake8..."
	$(FLAKE8) email_processor tests/
	@echo "🎨 Checking code formatting with black..."
	$(BLACK) --check email_processor tests/

# Format the code
format:
	@echo "🎨 Formatting code with black..."
	$(BLACK) email_processor tests

# Run the email processor
run:
	$(PYTHON) -m email_processor --config process_invoices.yaml

# Run example with DialogChain
run-example:
	@echo "📧 Starting email invoice processing example..."
	PYTHONPATH="/home/tom/github/dialogchain/python/src:${PYTHONPATH}" \
	$(PYTHON) -m examples.run_dialogchain_example

# Stop running example
stop-example:
	@echo "🛑 Stopping email processor..."
	@-pkill -f "python.*email_processor" || true

# View logs
view-logs:
	@echo "📋 Showing logs..."
	@if [ -d "logs" ]; then \
		find logs/ -type f -name "*.log" -exec tail -f {} +; \
	else \
		echo "No logs directory found."; \
	fi

# Setup environment variables
setup-env:
	@if [ ! -f ".env" ]; then \
		echo "Creating .env file from example..."; \
		cp .env.example .env; \
		echo "Please edit the .env file with your configuration"; \
	else \
		echo ".env file already exists"; \
	fi

# Clean up
clean:
	@echo "🧹 Cleaning up..."
	find . -type d -name '__pycache__' -exec rm -rf {} +
	find . -type f -name '*.py[co]' -delete
	find . -type d -name '.mypy_cache' -exec rm -rf {} +
	find . -type d -name '.pytest_cache' -exec rm -rf {} +
	rm -rf *.egg-info/ build/ dist/ .coverage htmlcov/

# Default target
.DEFAULT_GOAL := help
