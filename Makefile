SHELL = /bin/bash

# See https://kodfabrik.com/journal/a-good-makefile-for-go#help
help: Makefile
	@echo
	@echo "Choose a command run in RAD:"
	@echo
	@sed -n 's/^##//p' $< | column -t -s ':' |  sed -e 's/^/ /'
	@echo

## build-and-run: Builds and runs the docker image
build-and-run:
	docker compose up -d --build

## container-clean: delete and volumes containers
clean:
	@echo "[NOTE] Removing running containers and shared volumes..."
	docker-compose down -v --remove-orphans

## container-stop: stop containers
stop:
	@echo "[NOTE] Stopping running containers..."
	docker-compose stop