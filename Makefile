.PHONY: build up create-db test-db clean down tests build redis-cli bash

build:
	COMPOSE_DOCKER_CLI_BUILD=1 DOCKER_BUILDKIT=1 docker-compose build

build-tests:
	COMPOSE_DOCKER_CLI_BUILD=1 DOCKER_BUILDKIT=1 \
		docker-compose -f docker-compose.tests.yml build

tests:
	docker-compose -f docker-compose.tests.yml run server tests

up:
	COMPOSE_DOCKER_CLI_BUILD=1 DOCKER_BUILDKIT=1 docker-compose up -d --build

create-db:
	docker-compose run server create_tables

shell:
	docker-compose run --rm server bash

redis-cli:
	docker-compose run --rm redis redis-cli -h redis
