# DialogChain Basic Examples

This directory contains basic examples demonstrating core DialogChain functionality.

## Examples

### 1. Simple Timer to Log
- **File**: `timer_to_log.yaml`
- **Description**: Demonstrates a basic timer that logs messages at regular intervals.
- **Run Command**: `make timer-to-log`

### 2. HTTP Request Handler
- **File**: `http_handler.yaml`
- **Description**: A simple HTTP server that responds to requests.
- **Run Command**: `make http-handler`

### 3. File Watcher
- **File**: `file_watcher.yaml`
- **Description**: Watches a directory for new files and processes them.
- **Run Command**: `make file-watcher`

## Prerequisites

- Python 3.8+
- DialogChain installed in development mode
- Required Python packages (install with `make deps`)

## Quick Start

1. Install dependencies:
   ```bash
   make deps
   ```

2. Run an example:
   ```bash
   make timer-to-log
   ```

3. View available make targets:
   ```bash
   make help
   ```

## Directory Structure

```
basic/
├── README.md          # This file
├── Makefile           # Makefile with useful commands
├── .env.example       # Example environment variables
├── input/             # Input directory for file watcher example
├── output/            # Output directory for processed files
├── timer_to_log.yaml  # Timer to log example
├── http_handler.yaml  # HTTP handler example
└── file_watcher.yaml  # File watcher example
```

## Environment Variables

Copy `.env.example` to `.env` and modify as needed:

```bash
cp .env.example .env
```

## License

MIT
