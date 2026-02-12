#!/bin/bash
# Script to initialize Ollama models
# Run this after Ollama service is deployed

# Wait for Ollama to be ready
echo "Waiting for Ollama service to start..."
sleep 30

# Pull the model
echo "Pulling llama3.2 model..."
curl -X POST http://localhost:11435/api/pull -d '{"name": "llama3.2"}'

echo "Ollama setup complete!"