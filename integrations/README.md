# Integration Examples

This directory contains examples of integrating DialogChain with various services and protocols.

## Available Integrations

- **MQTT** - Message Queuing Telemetry Transport examples
  - Basic MQTT publishing/subscribing
  - MQTT with file watching
  - MQTT pub/sub patterns

- **gRPC** - High-performance RPC framework
  - Basic gRPC service integration
  - Bidirectional streaming

- **HTTP** - Web service integrations
  - HTTP server endpoints
  - REST API integrations
  - Webhook handling

- **Email** - Email processing
  - Incoming email processing
  - Email notification sending

- **Web** - Web application integrations
  - Web form processing
  - API integrations

## Running Integration Examples

Each integration example can be run using the main Makefile:

```bash
# List all available integration examples
make list-examples | grep integrations/

# Run a specific integration example
make run-example EXAMPLE=integrations/mqtt/basic
```

## Prerequisites

- Docker and Docker Compose
- Required services (MQTT broker, gRPC server, etc.)
- Python dependencies (install with `make install`)

## Configuration

Most examples use environment variables for configuration. Copy `.env.example` to `.env` and update the values as needed.

## Troubleshooting

- Check container logs: `make view-logs`
- Verify service connectivity
- Check environment variable settings
