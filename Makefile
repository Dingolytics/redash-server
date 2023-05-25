.PHONY: build up create-db test-db clean down tests build redis-cli bash

build:
	COMPOSE_DOCKER_CLI_BUILD=1 DOCKER_BUILDKIT=1 \
	docker-compose build

up:
	docker compose up

test-build:
	COMPOSE_DOCKER_CLI_BUILD=1 DOCKER_BUILDKIT=1 \
	docker compose -f docker-compose.tests.yml build

test-createdb:
	docker compose -f docker-compose.tests.yml run --rm server create_tables

test: test-build test-createdb
	docker compose -f docker-compose.tests.yml run --rm server tests -x

createdb:
	docker compose run --rm server create_tables

shell:
	docker compose run --rm server bash

redis-cli:
	docker compose run --rm redis redis-cli -h redis
