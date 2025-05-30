# DialogChain Examples

This directory contains various example configurations demonstrating different features and use cases of DialogChain.

## Table of Contents

1. [Basic Examples](#basic-examples)
2. [File Processing](#file-processing)
3. [Messaging & Integration](#messaging--integration)
4. [Advanced Examples](#advanced-examples)
5. [Tutorial Examples](#tutorial-examples)
6. [Running Examples](#running-examples)

## Basic Examples

### `basic_timer.yaml`
A simple timer that logs "Hello, World!" every 5 seconds.

**Features:**
- Basic timer configuration
- Simple message templating
- Logging output

**Usage:**
```bash
python -m dialogchain run --config examples/basic_timer.yaml
```

### `simple_timer.yaml`
Basic timer example with structured JSON output.

**Features:**
- Structured JSON output
- Dynamic timestamp inclusion
- Configurable interval

### `hello_world.yaml`
Minimal "Hello World" example demonstrating the simplest possible DialogChain configuration.

## File Processing

### `file_watcher_example.yaml`
Watches a file for changes and processes its contents.

**Features:**
- File system monitoring
- Content extraction
- Line and word counting

**Dependencies:**
- File system access to the monitored file

### `file_to_mqtt_example.yaml`
Monitors a file and publishes changes to an MQTT topic.

**Features:**
- File system integration
- MQTT publishing
- Content transformation

**Dependencies:**
- MQTT broker
- File system access

### `json_processor_example.yaml`
Processes JSON files with multiple transformation steps.

**Features:**
- JSON parsing
- Multi-step transformations
- Conditional processing

## Messaging & Integration

### `mqtt_pubsub_example.yaml`
Implements MQTT publisher and subscriber functionality.

**Features:**
- MQTT publishing and subscribing
- Topic-based routing
- Message transformation

**Dependencies:**
- MQTT broker

### `http_handler.yaml`
Sets up an HTTP endpoint for receiving and processing requests.

**Features:**
- HTTP server
- Request/response handling
- URL routing

### `grpc_routes.yaml`
Demonstrates gRPC service integration.

**Features:**
- gRPC server
- Protocol Buffers
- Service definitions

**Dependencies:**
- gRPC tools
- Protocol buffer definitions

## Advanced Examples

### `complex_example.yaml`
Combines multiple routes and processors for a complete workflow.

**Features:**
- Multiple routes
- Complex transformations
- Error handling

### `structured_timer_example.yaml`
Generates and processes structured sensor data.

**Features:**
- Structured data generation
- Conditional processing
- Data enrichment

### `camera_routes.yaml`
Video processing pipeline example.

**Features:**
- Video capture
- Frame processing
- Real-time analysis

**Dependencies:**
- OpenCV
- Camera access

### `iot_routes.yaml`
IoT device communication patterns.

**Features:**
- Device management
- Data collection
- Command handling

## Tutorial Examples

### `basic/` Directory
Contains basic examples for getting started:
- `basic_usage_dsl.yaml`: Basic DSL usage
- `file_watcher.yaml`: Simple file watching
- `http_handler.yaml`: Basic HTTP handling
- `timer_to_log.yaml`: Timer to log example

### `email-invoices/` Directory
Example for processing email invoices.

**Features:**
- Email parsing
- Attachment handling
- Data extraction

### `web-invoices/` Directory
Example for processing web-based invoices.

**Features:**
- Web scraping
- Form handling
- Data extraction

## Running Examples

### Prerequisites
- Python 3.8+
- DialogChain installed (`pip install -e .` from project root)
- Additional dependencies as specified in each example

### Basic Usage
```bash
# Run a specific example
python -m dialogchain run --config examples/example_name.yaml

# Run with verbose output
python -m dialogchain run --config examples/example_name.yaml -v
```

### Using Docker
For examples requiring additional services:
```bash
# Start required services
docker-compose -f docker-compose.test.yml up -d

# Run the example
python -m dialogchain run --config examples/example_name.yaml
```

## Troubleshooting

1. **Missing Dependencies**
   - Install required Python packages: `pip install -r requirements.txt`
   - For MQTT examples, ensure an MQTT broker is running
   - For camera examples, ensure camera access is properly configured

2. **Permission Issues**
   - Ensure read/write permissions for file operations
   - Check service account permissions for cloud integrations

3. **Debugging**
   - Use `-v` flag for verbose output
   - Check log files in the configured log directory
   - Verify network connectivity for remote services

## Contributing

When adding new examples:
1. Follow the existing naming conventions
2. Include clear comments in configuration files
3. Document any external dependencies
4. Update this documentation
5. Add tests when applicable
