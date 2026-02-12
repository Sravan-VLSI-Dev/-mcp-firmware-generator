# Dockerfile for Ollama service
FROM ollama/ollama:latest

# Set environment variables
ENV OLLAMA_HOST=0.0.0.0
ENV OLLAMA_PORT=11435
ENV PORT=11435

# Expose port
EXPOSE 11435

# Start Ollama first in the background, then pull model
CMD sh -c 'ollama serve & sleep 10 && ollama pull llama3.2 && wait'