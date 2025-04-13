FROM python:3.8-slim-buster

WORKDIR /app

RUN apt-get update && \
    apt-get -y install gcc mono-mcs git swi-prolog docker.io && \
    rm -rf /var/lib/apt/lists/*

RUN curl -sSL https://get.docker.com/ | sh

COPY . .
RUN pip3 install poetry
RUN chmod +x install.sh
RUN ./install.sh
