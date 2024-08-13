# /bin/bash
ollama serve & \
    sleep 10 && \
    ollama pull llama3.1 && \
    ollama pull llava && \
    npm install --force && \
    npm run build && \
    npm start;