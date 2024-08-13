# ollama.sh
ollama serve & \
    sleep 10 && \
    ollama pull llama3.1 && \
    ollama pull llava && \
    tail -f /dev/null;