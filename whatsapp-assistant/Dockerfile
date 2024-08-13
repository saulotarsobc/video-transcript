# Dockerfile.ollama
FROM node:20

RUN apt-get update && \
    apt-get install -y \
    wget \
    gnupg \
    ca-certificates \
    libgtk-3-0 \
    libx11-xcb1 \
    libxcomposite1 \
    libxdamage1 \
    libxrandr2 \
    libgbm1 \
    libasound2 \
    libpangocairo-1.0-0 \
    libnss3 \
    libxss1 \
    libx11-6 \
    libxcursor1 \
    libxinerama1 \
    libxkbcommon0 \
    libglu1-mesa \
    fonts-liberation \
    libappindicator3-1 \
    xdg-utils \
    libatk-bridge2.0-0 \
    libcups2 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*;

WORKDIR /app

COPY /package.json package.json
COPY /package-lock.json package-lock.json
COPY /src src
COPY /tsconfig.json tsconfig.json
COPY /prisma prisma
COPY /.env.prod .env
COPY /ollama.sh ollama.sh

RUN curl -fsSL https://ollama.com/install.sh | sh;

ENTRYPOINT ["sh", "ollama.sh"]
# CMD [ "tail", "-f", "/dev/null" ]
