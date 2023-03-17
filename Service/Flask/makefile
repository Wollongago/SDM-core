.PHONY: up down logs test clear stop restart bash

export UID:=$(shell id -u)
export GID:=$(shell id -g)

default:
	@echo "Default target"

build:
	@echo "============= Building Flask image ============="
	test -n "$(VERSION)"  # $$VERSION
	docker build --label sb.flask.version=${VERSION} \
	-t sb/flask:${VERSION} \
	-t sb/flask:latest \
	-f Dockerfile .	

up:
	@echo "============= Sarting Webstack ============="
	@docker network inspect sb-net >/dev/null || docker network create -d bridge --subnet 42.42.0.0/24 --gateway 42.42.0.1 sb-net
	docker-compose -p sb up -d

stop:
	@echo "============= Stopping http ============="
	docker-compose -p sb stop flask-http

restart:
	@echo "============= Restart http ============="

	@LOGPATH=$$(docker inspect --format='{{.LogPath}}' sb-flask-http-1); \
	if [ -n "$${LOGPATH}" ]; then sudo truncate -s 0 $${LOGPATH}; fi
	docker-compose -p sb restart flask-http

reload:
	@echo "============= Reload http server ============="
	@docker exec -it $$(docker ps -aqf "name=sb-flask-http-1") /bin/bash -c 'kill -HUP `cat /tmp/http.pid`'

down:
	@echo "============= Shutdown Everything ============="
	docker-compose -p sb down --remove-orphans

logs:
	@echo "============= Logs of http ============="
	docker-compose -p sb logs -f flask-http

bash:
	@echo "============= Entering Flask bash shell as $(UID):$(GID) ============="
	@docker exec --user $(UID):$(GID) -it $$(docker ps -aqf "name=sb-flask-http-1") /bin/bash