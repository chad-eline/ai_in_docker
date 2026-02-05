SHELL = /bin/bash

# See https://kodfabrik.com/journal/a-good-makefile-for-go#help
help: Makefile
	@echo
	@echo "Choose a command run in RAD:"
	@echo
	@sed -n 's/^##//p' $< | column -t -s ':' |  sed -e 's/^/ /'
	@echo

## build-and-run: Builds and runs Docker containers (default: no proxy)
build-and-run:
	docker compose up -d --build

## build-and-run-with-proxy: Builds and runs with network proxy enabled (test offline mode)
build-and-run-with-proxy:
	docker compose --profile with-proxy up -d --build

## py-setup: Create virtual environment and install Python dependencies (requires uv)
py-setup:
	@echo "[NOTE] Setting up Python environment with uv..."
	uv venv
	@echo "[NOTE] Installing dependencies..."
	uv sync
	@echo "[NOTE] Python setup complete. Activate with: source .venv/bin/activate"

## py-agent: Run the AI agent scaffold (make sure containers are running)
py-agent:
	uv run agent.py

## py-clean: Remove Python virtual environment and caches
py-clean:
	rm -rf .venv
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

## logs-ollama: Show Ollama container logs
logs-ollama:
	docker compose logs -f ollama

## logs-webui: Show Open-webui container logs
logs-webui:
	docker compose logs -f open-webui

## logs-proxy: Show proxy container logs (only if running with proxy profile)
logs-proxy:
	docker compose logs -f proxy

## logs-all: Show all container logs
logs-all:
	docker compose logs -f

## container-clean: delete and volumes containers
clean:
	@echo "[NOTE] Removing running containers and shared volumes..."
	docker compose down -v --remove-orphans

## container-stop: stop containers
stop:
	@echo "[NOTE] Stopping running containers..."
	docker compose stop