.PHONY: build up create-db test-db clean down tests build redis-cli bash

build:
	COMPOSE_DOCKER_CLI_BUILD=1 DOCKER_BUILDKIT=1 docker-compose build

up:
	COMPOSE_DOCKER_CLI_BUILD=1 DOCKER_BUILDKIT=1 docker-compose up -d --build

down:
	docker-compose down

clean:
	docker-compose down && docker-compose rm

create-db:
	docker-compose run server create_tables

test-db:
	@for i in `seq 1 5`; do \
		if (docker-compose exec postgres sh -c 'psql -U postgres -c "select 1;"' 2>&1 > /dev/null) then break; \
		else echo "postgres initializing..."; sleep 5; fi \
	done
	docker-compose exec postgres sh -c 'psql -U postgres -c "drop database if exists tests;" && psql -U postgres -c "create database tests;"'

tests:
	POSTGRES_DB=tests PGDATA_VOLUME=pgdata15-tests \
		docker-compose run server tests

redis-cli:
	docker-compose run --rm redis redis-cli -h redis

bash:
	docker-compose run --rm server bash
