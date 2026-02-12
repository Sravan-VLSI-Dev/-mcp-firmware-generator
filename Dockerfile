# Dockerfile for Ollama service
FROM ollama/ollama:latest

# Expose port
EXPOSE 11435

# Set environment variables
ENV OLLAMA_HOST=0.0.0.0
ENV OLLAMA_PORT=11435

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
  CMD curl -f http://localhost:11435/ || exit 1

# Start Ollama
CMD ["ollama", "serve"]