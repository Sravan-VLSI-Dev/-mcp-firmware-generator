# Dockerfile for Ollama service
FROM ollama/ollama:latest

# Set environment variables
ENV OLLAMA_HOST=0.0.0.0
ENV OLLAMA_PORT=11435

# Expose port
EXPOSE 11435

# Start Ollama
CMD ["serve"]