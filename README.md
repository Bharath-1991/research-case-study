# Simple Project
 > This is a simple project to demonstrate how to build a simple Flask RESTful API with Docker-Compose.

## What is this project about?

This is the project that was used to create as part of POC on how to create a simpleFlask RESTful API with Docker-Compose with backend as mongodb(key store).

## Requirements

To build this project you will need:-
    1. Docker
    2. Docker-compose
    3. Pytest (to run unit tests)

## Deploy and Run

After cloning this repository, you can type the following command to start the simple app:

## Composes project using docker-compose

	docker-compose -f deployments/docker-compose.yml build
	docker-compose -f deployments/docker-compose.yml down -v
	docker-compose -f deployments/docker-compose.yml up -d --force-recreate

Then simply visit [localhost:5000][App] !


[Docker Install]:  https://docs.docker.com/install/
[Docker Compose Install]: https://docs.docker.com/compose/install/
[App]: http://127.0.0.1:5000

