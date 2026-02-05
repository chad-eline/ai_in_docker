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
	uv run src/agent.py

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

## logs-mcp: Show MCP server container logs
logs-mcp:
	docker compose logs -f mcp-server

## logs-all: Show all container logs
logs-all:
	docker compose logs -f

## mcp-restart: Restart the MCP server container
mcp-restart:
	docker compose restart mcp-server

## mcp-docs: Open MCP server API documentation in browser
mcp-docs:
	@echo "Opening MCP API docs at http://localhost:8000/docs"
	@xdg-open http://localhost:8000/docs 2>/dev/null || open http://localhost:8000/docs 2>/dev/null || echo "Visit: http://localhost:8000/docs"

## mcp-test: Test MCP server is running and list available tools
mcp-test:
	@echo "Testing MCP server..."
	@curl -s http://localhost:8000/openapi.json | python3 -c "import sys,json; d=json.load(sys.stdin); print('Available tools:'); [print(f'  - {p}') for p in d.get('paths',{}).keys() if p != '/']" 2>/dev/null || echo "MCP server not running. Start with: make build-and-run"

## backup: Backup Open-webui data (conversations, settings, notes) to a tar file
backup:
	@echo "[NOTE] Backing up Open-webui data..."
	@mkdir -p backups
	docker run --rm -v ai_in_docker_openwebui_data:/data -v $(PWD)/backups:/backup alpine tar cvf /backup/openwebui-backup-$$(date +%Y%m%d-%H%M%S).tar -C /data .
	@echo "[NOTE] Backup saved to backups/"
	@ls -lh backups/*.tar | tail -1

## restore: Restore Open-webui data from the latest backup (or specify BACKUP=filename)
restore:
	@echo "[NOTE] Restoring Open-webui data..."
	@if [ -z "$(BACKUP)" ]; then \
		BACKUP_FILE=$$(ls -t backups/*.tar 2>/dev/null | head -1); \
	else \
		BACKUP_FILE="backups/$(BACKUP)"; \
	fi; \
	if [ -z "$$BACKUP_FILE" ] || [ ! -f "$$BACKUP_FILE" ]; then \
		echo "[ERROR] No backup file found. Run 'make backup' first or specify BACKUP=filename"; \
		exit 1; \
	fi; \
	echo "[NOTE] Restoring from: $$BACKUP_FILE"; \
	docker run --rm -v ai_in_docker_openwebui_data:/data -v $(PWD)/backups:/backup alpine sh -c "rm -rf /data/* && tar xvf /backup/$$(basename $$BACKUP_FILE) -C /data"
	@echo "[NOTE] Restore complete. Restart containers with: make build-and-run"

## container-clean: delete and volumes containers
clean:
	@echo "[NOTE] Removing running containers and shared volumes..."
	docker compose down -v --remove-orphans

## container-stop: stop containers
stop:
	@echo "[NOTE] Stopping running containers..."
	docker compose stop