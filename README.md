# Awkward π-nguin (APi)

Microservice orchestration language

## How to contribute

After forking the repository create a new branch using:

```
./build.sh -b <your-branch-name>
```

After editing code to commit and push use:

```
./build.sh -c "<commit-message>" <your-branch-name>
```

Create a pull request at [APi Github repository](https://github.com/AILab-FOI/APi) and please describe what the pull request has done or mention an appropriate issue (i.e. #3).

## Run as Dockerized container

Running Dockerized containers provides full support to running services locally. The docker compose starts up:

- prosody server -- which enables XMPP communication (takes away the hurdle of registering accounts)
- python3 environment -- which comes with installed prerequisites required to run the application

The dockerized containers are meant to be used for the development phase, hence the python3 environment reads files current directory and supports hot reload, so that any changes made to the files may immediately be executed from the environment.

Run the following steps to start up the dockerized environment:

1. `docker-compose up -d` -- which shall download & build the containers
2. `docker exec -ti api /bin/bash` -- to bash into the python3 environment
3. From inside the bash shell: `python3 APi.py basic.api` -- in order to run the application with the communication flows specification file
4. To view live prosody logs, which might be helpful as they preview connections, run: `docker logs -f --tail 10 prosody`
