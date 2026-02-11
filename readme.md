# AI Docker Examples

A simple environment to experiment with AI models locally using a ChatGPT-style
web interface.

## Quick Start

1. **Prerequisites:** Docker Desktop running, WSL (on Windows)

2. **Build and run:**
   ```bash
   make build-and-run
   ```

3. **Open the web UI:** http://localhost:3000

4. **Select a model** from the dropdown and start chatting!

## Features

- **Local LLMs:** Mistral 7B, Llama 3, Phi-3 Mini (runs offline)
- **ChatGPT-style UI:** Open-webui with conversations, notes, and knowledge bases
- **MCP Tools:** File access, Python execution, and more
- **Optional proxy:** Test true offline capability with network restrictions

## Project Structure

```
.
├── docker-compose.yml      # Container orchestration
├── Dockerfile              # Ollama container
├── Dockerfile.mcp          # MCP server container
├── Makefile                # Convenience commands
├── src/                    # Python source files
│   ├── agent.py            # AI agent scaffold
│   ├── chat_mistral.py     # Direct model interaction
│   └── mcp_server.py       # MCP tools implementation
├── pyproject.toml          # Python dependencies
└── docs/                   # Documentation
```

## Common Commands

| Command                      | Description                        |
| ---------------------------- | ---------------------------------- |
| `make build-and-run`         | Build and start all containers     |
| `make stop`                  | Stop all containers                |
| `make logs-all`              | View all container logs            |
| `make backup`                | Backup Open-webui data             |
| `make restore`               | Restore from backup                |
| `make clean`                 | Remove containers and volumes      |

## Documentation

| Topic | Description |
| ----- | ----------- |
| [API Reference](docs/api-reference.md) | Service URLs and endpoint documentation |
| [Tools & Technologies](docs/tools.md) | WSL, Docker, Ollama, Open-webui, TinyProxy |
| [Models](docs/models.md) | Available models and how to add more |
| [MCP Server](docs/mcp-server.md) | Tool integration, setup, and custom tools |
| [Python Development](docs/python-development.md) | uv setup, agent development |
| [Backup & Restore](docs/backup-restore.md) | Data persistence and recovery |
| [Troubleshooting](docs/troubleshooting.md) | Common issues and solutions |

## Health Checks

All services include health checks for reliable startup:

- **Ollama:** Checks model list availability
- **Open-webui:** Checks web server on port 8080
- **MCP Server:** Checks API endpoint

Open-webui waits for Ollama and MCP server to be healthy before starting.

## Security Notes

- First user to register becomes admin - set a strong password
- Models run locally - no data sent to external services
- MCP tools are sandboxed with path and execution restrictions

## Next Steps

- Set up [MCP tools](docs/mcp-server.md) for enhanced capabilities
- Create [custom models](docs/mcp-server.md#custom-models-with-pre-enabled-tools) with pre-enabled tools
- Explore the [Python agent](docs/python-development.md) for programmatic access
