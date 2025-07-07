FROM python:3.11-slim

RUN apt-get update && apt-get install -y python3 python3-pip

RUN apt-get update && apt-get install -y curl

RUN apt-get update && apt-get install -y bash

# Download Ollama CLI (adjust if different path is required)
# RUN curl -fsSL https://ollama.com/install.sh -o /usr/local/bin/ollama && \
#     chmod +x /usr/local/bin/ollama

RUN curl -fsSL https://ollama.com/install.sh | sh

WORKDIR /app

# Copy your script and modelfile
COPY test_ollama.py Modelfile /app/

COPY ./docker/entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

RUN pip install requests

ENTRYPOINT ["/app/entrypoint.sh"]

