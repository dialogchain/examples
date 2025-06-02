.PHONY: help setup install test run clean lint format typecheck dev-requirements

# Project variables
PROJECT_NAME = email-invoice-processor
PYTHON = python3
PIP = pip3
VENV = venv
PYTHON_VENV = $(VENV)/bin/python
PIP_VENV = $(VENV)/bin/pip
PYTEST = $(VENV)/bin/pytest
FLAKE8 = $(VENV)/bin/flake8
BLACK = $(VENV)/bin/black
ISORT = $(VENV)/bin/isort
MYPY = $(VENV)/bin/mypy

# Help message
help:
	@echo "\n\033[1m$(PROJECT_NAME) - Makefile Help\033[0m"
	@echo "\nAvailable targets:"
	@echo "  make help         - Show this help message"
	@echo "  make setup        - Set up the development environment"
	@echo "  make install      - Install the package in development mode"
	@echo "  make test         - Run tests"
	@echo "  make lint         - Run code style checks"
	@echo "  make typecheck    - Run type checking"
	@echo "  make format       - Format the code"
	@echo "  make run          - Run the email processor"
	@echo "  make clean        - Clean up temporary files"

# Setup development environment
setup: venv requirements-dev.txt
	$(PIP_VENV) install -U pip setuptools wheel
	$(PIP_VENV) install -r requirements-dev.txt
	$(PIP_VENV) install -e .

# Create virtual environment
venv:
	if [ ! -d "$(VENV)" ]; then \
		$(PYTHON) -m venv $(VENV) && \
		. $(VENV)/bin/activate && \
		$(PIP) install --upgrade pip; \
	fi

# Install the package in development mode
install:
	$(PIP_VENV) install -e .

# Run tests
test:
	$(PYTEST) tests/ -v --cov=email_processor --cov-report=term-missing

# Run code style checks
lint:
	$(FLAKE8) email_processor tests
	$(BLACK) --check email_processor tests
	$(ISORT) --check-only email_processor tests

# Run type checking
typecheck:
	$(MYPY) email_processor

# Format the code
format:
	$(BLACK) email_processor tests
	$(ISORT) email_processor tests

# Run the email processor
run:
	$(PYTHON) -m email_processor --config process_invoices.yaml

# Stop Docker containers and remove volumes
stop:
	@echo "Stopping all Docker containers and removing volumes..."
	@docker-compose -f ../docker-compose.yml down -v --remove-orphans || true
	@echo "✅ All Docker containers stopped and volumes removed"

# Clean up
clean: stop
	find . -type d -name '__pycache__' -exec rm -rf {} +
	find . -type f -name '*.pyc' -delete
	find . -type f -name '*.pyo' -delete
	find . -type d -name '.mypy_cache' -exec rm -rf {} +
	find . -type d -name '.pytest_cache' -exec rm -rf {} +
	find . -type d -name '.coverage' -delete
	find . -type d -name 'htmlcov' -exec rm -rf {} +
	find . -type d -name '*.egg-info' -exec rm -rf {} +

# Generate development requirements
dev-requirements: requirements-dev.txt

requirements-dev.txt: requirements.txt
	echo "-r requirements.txt" > requirements-dev.txt
	echo "\n# Development dependencies" >> requirements-dev.txt
	echo "pytest==7.4.0" >> requirements-dev.txt
	echo "pytest-cov==4.1.0" >> requirements-dev.txt
	echo "flake8==6.1.0" >> requirements-dev.txt
	echo "black==23.7.0" >> requirements-dev.txt
	echo "isort==5.12.0" >> requirements-dev.txt
	echo "mypy==1.5.0" >> requirements-dev.txt
	echo "types-requests==2.31.0.1" >> requirements-dev.txt

# Default target
.DEFAULT_GOAL := help



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
