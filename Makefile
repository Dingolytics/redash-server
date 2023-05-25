.PHONY: build up create-db test-db clean down tests build redis-cli bash

COMPOSE_CMD := docker compose

TEST_COMPOSE_CMD := docker compose -f docker-compose.tests.yml

build:
	$(COMPOSE_CMD) build

up:
	$(COMPOSE_CMD) up

createdb:
	$(COMPOSE_CMD) run --rm server create_tables

shell:
	$(COMPOSE_CMD) run --rm server bash

redis-cli:
	$(COMPOSE_CMD) run --rm redis redis-cli -h redis

test-build:
	$(TEST_COMPOSE_CMD) build

test-createdb:
	$(TEST_COMPOSE_CMD) run --rm server-tests create_tables

test: test-build test-createdb
	$(TEST_COMPOSE_CMD) run --rm server-tests
