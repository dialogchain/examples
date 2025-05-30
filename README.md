# DialogChain Examples

This directory contains example configurations for DialogChain, demonstrating various features and integration patterns. Each example is designed to showcase different capabilities of the DialogChain system.

## 📋 Table of Contents

- [Getting Started](#-getting-started)
- [Basic Examples](#-basic-examples)
- [File Processing](#-file-processing)
- [Network & API](#-network--api-integrations)
- [Advanced Features](#-advanced-features)
- [Running Examples](#-running-examples)
- [Contributing](#-contributing)

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- DialogChain installed (see main [README](../python/README.md))
- Any additional dependencies for specific examples

### Running Examples

Most examples can be run using the `dialogchain` CLI:

```bash
# Run a specific example
dialogchain serve examples/simple_timer.yaml

# Run with debug logging
DIALOGCHAIN_LOG_LEVEL=debug dialogchain serve examples/simple_timer.yaml
```

## 🧩 Basic Examples

### Hello World
- **File**: `hello_world.yaml`
- **Description**: Minimal example to verify your setup
- **Features**: Basic pipeline, logging
- **Run**: `dialogchain serve examples/hello_world.yaml`

### Simple Timer
- **File**: `simple_timer.yaml`
- **Description**: Logs structured JSON data at regular intervals
- **Features**: Timers, structured logging
- **Run**: `dialogchain serve examples/simple_timer.yaml`

### Logging Example
- **File**: `simple_logging_example.yaml`
- **Description**: Demonstrates different log levels and outputs
- **Features**: Logging configuration, log levels
- **Run**: `dialogchain serve examples/simple_logging_example.yaml`

## 📂 File Processing

### File Watcher
- **File**: `file_watcher_example.yaml`
- **Description**: Monitors a file for changes and processes its contents
- **Features**: File system monitoring, content processing
- **Prerequisites**: Create an `input/` directory
- **Run**: `dialogchain serve examples/file_watcher_example.yaml`

### JSON Processor
- **File**: `json_processor_example.yaml`
- **Description**: Processes and transforms JSON data
- **Features**: JSON parsing, data transformation
- **Run**: `dialogchain serve examples/json_processor_example.yaml`

## 🌐 Network & API Integrations

### HTTP Server
- **File**: `http_handler.yaml`
- **Description**: Sets up an HTTP endpoint
- **Features**: HTTP server, request handling
- **Run**: `dialogchain serve examples/http_handler.yaml`
- **Test**: `curl http://localhost:8080/hello`

### MQTT Pub/Sub
- **File**: `mqtt_pubsub_example.yaml`
- **Description**: Implements MQTT publisher and subscriber
- **Features**: MQTT integration, message brokering
- **Prerequisites**: MQTT broker (e.g., Mosquitto)
- **Run**: `dialogchain serve examples/mqtt_pubsub_example.yaml`

### gRPC Service
- **File**: `grpc_routes.yaml`
- **Description**: gRPC service implementation
- **Features**: gRPC server, protocol buffers
- **Run**: `dialogchain serve examples/grpc_routes.yaml`

## 🚀 Advanced Features

### Camera Integration
- **File**: `camera_routes.yaml`
- **Description**: Captures and processes video streams
- **Features**: OpenCV integration, video processing
- **Prerequisites**: OpenCV, camera access
- **Run**: `dialogchain serve examples/camera_routes.yaml`

### IoT Device Control
- **File**: `iot_routes.yaml`
- **Description**: Controls IoT devices
- **Features**: Device management, state handling
- **Run**: `dialogchain serve examples/iot_routes.yaml`

## 🛠️ Running Examples

### Using Docker

```bash
# Build the container
docker build -t dialogchain-examples .

# Run an example
docker run -it --rm -v $(pwd):/app dialogchain-examples dialogchain serve examples/hello_world.yaml
```

### Debugging

Set environment variables for debugging:

```bash
# Enable debug logging
DIALOGCHAIN_LOG_LEVEL=debug dialogchain serve examples/your_example.yaml

# Enable development mode (auto-reload on changes)
DIALOGCHAIN_DEV=1 dialogchain serve examples/your_example.yaml
```

## 🤝 Contributing

We welcome contributions to our examples! Please see the main [Contributing Guide](../CONTRIBUTING.md) for details.

1. Fork the repository
2. Create a new branch for your example
3. Add your example with appropriate documentation
4. Submit a pull request

## 📄 License

These examples are part of the DialogChain project and are licensed under the [Apache 2.0 License](../LICENSE).

### Advanced Examples

1. **complex_example.yaml**
   - Combines multiple routes and processors
   - Demonstrates advanced routing and transformation

2. **structured_timer_example.yaml**
   - Generates and processes structured sensor data
   - Shows conditional processing and data enrichment

3. **camera_routes.yaml**
   - Video processing pipeline example
   - Demonstrates handling binary data streams

4. **iot_routes.yaml**
   - IoT device communication patterns
   - Shows device management and data collection

## Running Examples

### Prerequisites

- Python 3.8+
- Docker (for MQTT and other containerized services)
- Required Python packages (install with `pip install -r requirements.txt` in the project root)

### Basic Usage

```bash
# Run a specific example
python -m src.dialogchain.cli run --config examples/example_name.yaml

# Run with verbose output
python -m src.dialogchain.cli run --config examples/example_name.yaml -v
```

### Running with Docker

Some examples require additional services like MQTT brokers. Use the provided docker-compose file:

```bash
# Start required services
docker-compose -f docker-compose.test.yml up -d

# Run your example
python -m src.dialogchain.cli run --config examples/example_name.yaml
```

## Development

When creating new examples:

1. Follow the existing naming conventions
2. Include clear comments in the YAML files
3. Document any external dependencies
4. Update this README with a brief description of the new example

## Troubleshooting

- Ensure all required services are running for integration examples
- Check file permissions for file watcher examples
- Use the `-v` flag for verbose logging when debugging
- For MQTT issues, verify the broker is accessible and the topic permissions are correct
