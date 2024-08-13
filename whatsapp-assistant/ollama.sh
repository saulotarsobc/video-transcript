# /bin/bash

# Start the Ollama server in the background
ollama serve & \
    sleep 10 && \
    ollama pull llama3.1 && \
    ollama pull llava && \
    npm install --force && \
    npm run build && \
    npm start;
    # tail -f /dev/null;