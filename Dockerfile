FROM python:3.8-slim-buster

WORKDIR /app

RUN apt-get update && \
    apt-get -y install gcc mono-mcs git swi-prolog docker.io && \
    rm -rf /var/lib/apt/lists/*

RUN curl -sSL https://get.docker.com/ | sh

# COPY requirements.txt requirements.txt
# RUN pip3 install -r requirements.txt
# RUN pip3 install --upgrade aiohttp_jinja2
# RUN pip3 install spade==3.2.3
# RUN pip3 install xmltodict

RUN pip3 install poetry
COPY install.sh install.sh
RUN chmod +x install.sh
# RUN install.sh
