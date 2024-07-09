FROM python:3.10-slim

WORKDIR /app

COPY main.py .
COPY .env.production .env
COPY /utils utils

# System
# RUN apt update && apt upgrade -y;
# RUN apt install software-properties-common -y;
RUN apt update;
RUN apt install ffmpeg -y;
RUN apt-get clean && rm -rf /var/lib/apt/lists/*

# Python
RUN pip install numpy==1.23.5;
RUN pip install python-dotenv==1.0.1;
RUN pip install requests==2.32.3;
RUN pip install colorama==0.4.6;
RUN pip install -U openai-whisper;


# CMD ["tail", "-f", "/dev/null"]
CMD ["python", "main.py"]