# Awkward π-nguin (APi)

Microservice orchestration language

## Run as Dockerized container

Running Dockerized containers provides full support to running services locally. The docker compose starts up:

- prosody server -- which enables XMPP communication (takes away the hurdle of registering accounts)
- python3 environment -- which comes with installed prerequisites required to run the application

The dockerized containers are meant to be used for the development phase, hence the python3 environment reads files current directory and supports hot reload, so that any changes made to the files may immediately be executed from the environment.

Run the following steps to start up the dockerized environment:

1. `docker-compose up -d` -- which shall download & build the containers
2. `docker exec -ti api /bin/bash` -- to bash into the python3 environment
3. Create a copy of `.env.sample`, name it `.env` and adjust values accordingly
4. From inside the bash shell: `poetry run python3 src/main.py basic.api` -- in order to run the application with the communication flows specification file
5. To view live prosody logs, which might be helpful as they preview connections, run: `docker logs -f --tail 10 prosody`

## Running Dockererized agents inside the container

APi allows for running agents as Docker containers among other types (Unix & Kubernetes). This is achieved by having the root service (api service) having Docker installed inside. Additionally, the Docker socket is passed as volume to the root service, which essentially means that the container has access to Docker on the host machine. That means that if the dockerized APi containers starts up new Docker container, these new containers will be treated as siblings to the APi container.

Within this setup, there is an example on how to run APi that starts up dockerized agent. Below are steps needed to be able to run the agent.

1. Positionate to `docker` directory which will be used to build a new image that will contain a file to be read
2. Run `docker build -t api_docker_example .` which will build the image
3. Run APi as with unix approach `poetry run python3 src/main.py docker.api` -- it is a specificaiton that uses the dockerized agent

Similarily, you can create your own docker container, which communicates via STDINT / STDOUT and use it.

This work has been supported in full by the Croatian Science Foundation under the project number [IP-2019-04-5824](http://dragon.foi.hr:8888/ohai4games).
