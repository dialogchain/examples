# DialogChain Examples

This directory contains example configurations for DialogChain, demonstrating various features and integration patterns. Each example is designed to showcase different capabilities of the DialogChain system.

## Available Examples

### Basic Examples

1. **basic_timer.yaml**
   - A simple timer that logs "Hello, World!" every 5 seconds
   - Demonstrates basic timer functionality and logging

2. **simple_timer.yaml**
   - Basic timer example with structured JSON output
   - Shows how to generate and log structured data

3. **simple_logging_example.yaml**
   - Demonstrates different log levels and formatting
   - Shows how to configure logging destinations

4. **hello_world.yaml**
   - Minimal "Hello World" example
   - Good starting point for new users

### File Processing

1. **file_watcher_example.yaml**
   - Watches a file for changes and processes its contents
   - Extracts file metadata like line count and content

2. **file_to_mqtt_example.yaml**
   - Monitors a file and publishes changes to MQTT
   - Demonstrates file-to-MQTT integration

3. **json_processor_example.yaml**
   - Processes JSON files with multiple transformation steps
   - Shows complex data transformation capabilities

### Integration Examples

1. **mqtt_pubsub_example.yaml**
   - Implements MQTT publisher and subscriber
   - Demonstrates bi-directional MQTT communication

2. **http_handler.yaml**
   - Sets up an HTTP endpoint
   - Processes incoming HTTP requests

3. **grpc_routes.yaml**
   - gRPC service integration
   - Shows how to handle gRPC requests and responses

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
