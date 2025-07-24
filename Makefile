.PHONY: help build run stop clean logs test

# Default target
help:
	@echo "Available commands:"
	@echo "  build     - Build the Docker image"
	@echo "  run       - Run the application with docker-compose"
	@echo "  stop      - Stop the application"
	@echo "  clean     - Remove containers and images"
	@echo "  logs      - Show application logs"
	@echo "  test      - Test the API endpoints"
	@echo "  build-prod - Build production image"

# Build development image
build:
	docker-compose build

# Build production image
build-prod:
	docker build -f Dockerfile.prod -t sautidesk-model:prod .

# Run with docker-compose
run:
	docker-compose up -d

# Stop application
stop:
	docker-compose down

# Clean up
clean:
	docker-compose down --rmi all --volumes --remove-orphans
	docker system prune -f

# Show logs
logs:
	docker-compose logs -f

# Test API
test:
	@echo "Testing API endpoints..."
	@echo "Health check:"
	curl -s http://localhost:8000/health | jq .
	@echo "\nRoot endpoint:"
	curl -s http://localhost:8000/ | jq .
	@echo "\nTesting ticket generation:"
	curl -s -X POST http://localhost:8000/predict \
		-H "Content-Type: application/json" \
		-d '{"issue_text": "My electricity has been out since last night. Please help.", "max_length": 512, "temperature": 0.7}' | jq . 