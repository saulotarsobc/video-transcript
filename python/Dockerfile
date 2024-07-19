FROM python:3.10-slim

WORKDIR /app

COPY main.py .
COPY .env.production .env
COPY /utils utils
COPY /services services

# System
RUN apt update;
RUN apt install ffmpeg -y;
RUN apt-get clean && rm -rf /var/lib/apt/lists/*

# Dependencies
RUN pip install numpy==1.23.5;
RUN pip install python-dotenv;
RUN pip install requests;
RUN pip install -U openai-whisper;
RUN pip install ollama;
RUN pip install colorama;

# Ollama
RUN curl https://ollama.ai/install.sh | sh
RUN which ollama
RUN ollama serve & sleep 5 && ollama pull llama3


# CMD ["tail", "-f", "/dev/null"]
# Run the Python application
CMD ["sh", "-c", "ollama serve & python main.py"]