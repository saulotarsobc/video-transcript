FROM python:3.10-slim

WORKDIR /app

COPY main.py .
# COPY audio.wav .
COPY requirements-on-docker.txt requirements.txt
COPY .env.production .env
COPY /utils utils

# System
RUN apt update && apt upgrade -y;
RUN apt install software-properties-common -y;
RUN apt install ffmpeg -y;
RUN apt install python3-venv -y;
RUN apt-get clean && rm -rf /var/lib/apt/lists/*

# Python
RUN pip install -r requirements.txt;
# RUN pip install -U openai-whisper;
# RUN pip install numpy==1.23.5;
# RUN whisper --model_dir temp --model tiny audio.wav;

# prender termial para o container não fechar
# CMD ["tail", "-f", "/dev/null"]

# EXPOSE 8000

CMD ["python", "main.py"]