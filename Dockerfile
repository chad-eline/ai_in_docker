# Just use the official Ollama image
FROM ollama/ollama:latest

# Expose API port
EXPOSE 11434

# Default command
CMD ["ollama", "serve"]
