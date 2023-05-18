FROM python:3.8-slim-buster

WORKDIR /app

RUN apt-get update && \
    apt-get -y install gcc mono-mcs git swi-prolog docker.io && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
RUN pip3 install git+https://github.com/AILab-FOI/pyxf
