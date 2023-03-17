.PHONY: build bash

DB?=sb

default:
	@echo "Default target"
	
build:
	@echo "============= Building MongoDB ============="
	test -n "$(VERSION)" # $$VERSION
	docker build --label sb.mongodb.version:latest \
	-t sb-mongodb \
	-f Dockerfile .

bash:
	@echo "============= Entering MongoDB bash shell ============="
	@docker exec -it $$(docker ps -aqf "name=sb-mongodb-1") /bin/bash