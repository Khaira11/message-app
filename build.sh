#!/bin/bash

# Build and push Docker image
echo "Building Docker image..."
docker build -t your-username/webhook-test-app:latest .

echo "Pushing to Docker Hub..."
docker push your-username/webhook-test-app:latest

echo "Image built and pushed successfully!"
