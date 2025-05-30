# Advanced Examples

This directory contains advanced examples demonstrating complex DialogChain configurations and patterns.

## Available Advanced Examples

### Camera Integration
- Camera feed processing
- RTSP stream handling
- Image processing pipelines

### IoT Integration
- IoT device communication
- Sensor data processing
- Device control flows

### JSON Processing
- Complex JSON transformations
- Data validation
- Schema evolution

### Structured Data
- Complex event processing
- State management
- Workflow orchestration

## Running Advanced Examples

Each example includes its own configuration and can be run using the main Makefile:

```bash
# List all advanced examples
make list-examples | grep advanced/

# Run a specific advanced example
make run-example EXAMPLE=advanced/camera/feed_processor
```

## Prerequisites

- Docker and Docker Compose
- Additional hardware may be required for some examples (e.g., cameras for RTSP)
- Check individual example READMEs for specific requirements

## Configuration

Most examples use environment variables for configuration. Copy `.env.example` to `.env` in the example directory and update the values as needed.

## Troubleshooting

- Check container logs: `make view-logs`
- Verify all required services are running
- Check network connectivity between services
- Review example-specific documentation for known issues
