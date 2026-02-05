# AI Docker Examples

## Overview

This is a simple example of how to build and run AI models with a chat-gpt style
web interface. The objective is to create a simple environment to experiment and
evaluate different AI models locally.

## Tools

This project uses the following tools:

### [WSL](https://learn.microsoft.com/en-us/windows/wsl/install)

- Windows Subsystem for Linux

### [Docker Desktop](https://docs.docker.com/desktop/)

- Desktop GUI for the popular container platform.

### [Ollama](https://ollama.com/)

- Ollama is a model runtime environment for managing models.
- It is akin to docker but for AI models.

### [Open-webui](https://openwebui.com/)

- Open-webui is an open-source web ui, providing a chat-gpt style interface.
- It is designed to run and operate totally offline.

### TinyProxy

TinyProxy is a lightweight HTTP/HTTPS proxy server. In this setup, it is used to control and restrict outbound internet access from the AI containers. The proxy can be enabled or disabled using Docker Compose profiles.

**Whitelist Configuration:**
- Whitelisted destinations are defined in `tinyproxy-whitelist.txt`
- Default whitelisted destinations: DNS resolvers, HuggingFace, PyPI, and key model hosting sites
- Add additional domains to `tinyproxy-whitelist.txt` as needed

**Testing Offline Capability:**
If you would like to test if models are truly running locally with network restrictions, run:
```bash
docker compose --profile with-proxy up -d --build
```

Then interact with the models and watch the logs—if they respond without timeout, they're truly offline. Otherwise, the requests will be blocked by the proxy.

To disable the proxy (default mode):
```bash
docker compose up -d --build
```

## Models

The following models are pre-loaded into Open-webUI. You can select them in the drop
down in the top left corner once you're in the webapp.

### [Mistral 7B](https://huggingface.co/mistralai/Mistral-7B-v0.1)

Mistral 7B is a powerful, open-weight large language model designed for efficiency and strong performance on a wide range of tasks. Developed by [Mistral AI](https://mistral.ai/).

### [Llama 3](https://huggingface.co/meta-llama/Meta-Llama-3-8B)

Llama 3 is Meta's latest open large language model, offering improved reasoning and coding abilities. Developed by [Meta AI](https://ai.meta.com/llama/).

### [Phi-3 Mini](https://huggingface.co/microsoft/phi-3-mini-4k-instruct)

Phi-3 Mini is a compact, instruction-tuned language model optimized for efficiency and low resource usage. Developed by [Microsoft Research](https://www.microsoft.com/en-us/research/project/phi/).

## Setup and Configuration

### Using uv for Python Development

This project uses `uv` as the Python package manager. All dependencies are defined in `pyproject.toml` targeting Python 3.11+.

**Install uv:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Install project dependencies:**
```bash
make py-setup
```

Or manually:
```bash
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv sync
```

**To run the agent script locally:**
```bash
make py-agent
```

Or manually:
```bash
uv run agent.py
```

### Project Structure

- `docker-compose.yml` — Orchestrates Ollama, Open-webui, and optional proxy containers
- `Dockerfile` — Builds the Ollama container image
- `agent.py` — Simple AI agent scaffold for tool calling and MCP integration (Phase 2)
- `chat_mistral.py` — Direct Mistral model interaction using HuggingFace Transformers
- `tinyproxy.conf` — Proxy configuration
- `tinyproxy-whitelist.txt` — List of whitelisted destination domains for proxy filtering
- `pyproject.toml` — Python project configuration and dependencies (uv/pip)
- `Makefile` — Convenience commands for Docker operations
- `.gitignore` — Git ignore rules for Python projects

## Build and Run

1. Make sure Docker Desktop is up and running.
2. Build and start the containers:

```bash
make build-and-run
```

3. Open Open-webui in your browser: [http://localhost:3000](http://localhost:3000/auth?redirect=%2F)

4. Check Ollama API status: [http://localhost:11434/](http://localhost:11434/)

### With Proxy Enabled (Testing Offline Mode)

To test if models are truly local with network restrictions enabled:

```bash
make build-and-run-with-proxy
```

The proxy will restrict outbound connections to whitelisted destinations only. If the models respond, they're running locally.

### Docker Operations

**Stop containers:**
```bash
make stop
```

**View logs:**
```bash
make logs-ollama        # Show Ollama logs
make logs-webui         # Show Open-webui logs
make logs-all           # Show all container logs
```

**Clean up (remove containers and volumes):**
```bash
make clean
```

## Health Checks

Both `ollama` and `open-webui` services include health checks:

- **Ollama**: Checks API availability at `/api/tags` every 10 seconds
- **Open-webui**: Checks web server availability at port 8080 every 10 seconds

Open-webui depends on a healthy Ollama service before starting. This ensures reliable container orchestration and graceful startup sequences.

## Agent Development

The `agent.py` file provides a scaffold for building an AI agent with:

- Direct Ollama API integration
- Tool definition and execution framework
- Structured output handling with Pydantic
- Comments and TODOs for Phase 2 MCP server integration

**Example usage (make sure Ollama container is running):**
```bash
make py-agent
```

Or manually:
```bash
uv run agent.py
```

See `agent.py` for more details on tool definitions and extensibility.

## Troubleshooting

### Container won't start
Check logs:
```bash
make logs-ollama   # Check Ollama
make logs-webui    # Check Open-webui
make logs-all      # Check all
```

### Models taking too long to load
First startup downloads the model weights (~7GB for Mistral). Subsequent startups are faster.

### Proxy causing timeouts
If using `make build-and-run-with-proxy`, ensure required domains are whitelisted in `tinyproxy-whitelist.txt`

## Security Notes

**Open-webUI Default Credentials:**
- On first access to Open-webui, you will be prompted to create admin credentials
- The first user registered becomes the admin
- Ensure you set a strong password, as this interface has access to your local models
- For local-only deployments, consider network isolation

## Next Steps (Phase 2)

Planned enhancements:
- MCP (Model Context Protocol) server integration for sandboxed tool access
- Advanced agent workflows (reasoning loops, memory)
- Database and filesystem integrations
- API endpoint security and rate limiting
