# Docker Setup for SautiDesk Model API

This document provides instructions for running the SautiDesk Model API using Docker.

## Prerequisites

- Docker
- Docker Compose
- Make (optional, for using Makefile commands)

## Quick Start

### Using Makefile (Recommended)

```bash
# Build and run the application
make build
make run

# Test the API
make test

# View logs
make logs

# Stop the application
make stop

# Clean up
make clean
```

### Using Docker Compose Directly

```bash
# Build the image
docker-compose build

# Run the application
docker-compose up -d

# View logs
docker-compose logs -f

# Stop the application
docker-compose down
```

### Using Docker Directly

```bash
# Build the image
docker build -t sautidesk-model .

# Run the container
docker run -d -p 8000:8000 --name sautidesk-model sautidesk-model

# Test the API
curl http://localhost:8000/health
```

## Production Deployment

For production deployment, use the production Dockerfile:

```bash
# Build production image
docker build -f Dockerfile.prod -t sautidesk-model:prod .

# Run production container
docker run -d -p 8000:8000 --name sautidesk-model-prod sautidesk-model:prod
```

## Environment Variables

The following environment variables can be configured:

- `PYTHONUNBUFFERED=1` - Ensures Python output is sent straight to terminal
- `PYTHONDONTWRITEBYTECODE=1` - Prevents Python from writing .pyc files

## API Endpoints

Once running, the following endpoints are available:

- `GET /` - Root endpoint with API information
- `GET /health` - Health check with model status
- `POST /predict` - Ticket generation endpoint
- `GET /docs` - Interactive API documentation

## Example Usage

```bash
# Generate a ticket
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "issue_text": "My electricity has been out since last night. Please help.",
    "max_length": 512,
    "temperature": 0.7
  }'
```

## Troubleshooting

### Model Loading Issues

If the model fails to load, ensure the model files are present in the correct location:

- `notebooks/t5-ticket-output_final/checkpoint-45000/`

### Memory Issues

The application requires significant memory for the T5 model. Ensure your Docker environment has at least 2GB of RAM available.

### Port Conflicts

If port 8000 is already in use, modify the port mapping in `docker-compose.yml`:

```yaml
ports:
  - "8001:8000" # Use port 8001 on host
```

## Health Checks

The container includes health checks that verify the API is responding correctly. You can check the health status with:

```bash
docker inspect sautidesk-model | grep Health -A 10
```
