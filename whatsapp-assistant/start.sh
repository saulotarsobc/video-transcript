#!/bin/sh

# Start the Ollama server in the background
ollama serve &

# Wait for Ollama to fully start (adjust the sleep time as needed)
sleep 10

# Run your command or application
# Example to pull models:
ollama pull llama3
ollama pull llava

# Keep the container running
exec tail -f /dev/null
