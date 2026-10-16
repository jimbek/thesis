# Setup the ollama environment.
FROM ollama/ollama:latest

# Copy the ollama model file into the container.
COPY /scripts/OllamaServe.sh /OllamaServe.sh

# Start ollama in the background.
ENTRYPOINT ["/bin/sh", "/OllamaServe.sh"]