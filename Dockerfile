# Dockerfile for Ollama service
FROM ollama/ollama:latest

# Set environment variables
ENV OLLAMA_HOST=0.0.0.0
ENV OLLAMA_PORT=11435
ENV PORT=11435

# Expose port
EXPOSE 11435

# Pull model at startup
RUN ollama pull llama3.2

# Start Ollama
CMD ["serve"]