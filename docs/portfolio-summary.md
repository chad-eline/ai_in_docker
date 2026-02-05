# AI Docker Examples

## Project Summary

A containerized local AI development environment featuring multiple large
language models with a ChatGPT-style web interface, MCP (Model Context Protocol)
tool integration, and optional network isolation for true offline operation.

**Tech Stack:** Docker, Python 3.11+, Ollama, Open-webui, FastAPI, MCP

---

## The Challenge

Running AI models locally typically requires:
- Complex dependency management across different tools
- Manual configuration of model runtimes and web interfaces
- No standardized way to give models access to tools (file I/O, code execution)
- Difficulty verifying models truly run offline without external API calls

## The Solution

A Docker Compose-based environment that orchestrates multiple services with
health checks, automatic model loading, and tool integration—all with a single
`make build-and-run` command.

### Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Docker Network                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────┐  │
│  │   Ollama     │  │  Open-webui  │  │   MCP Server     │  │
│  │  (Models)    │◄─┤   (Web UI)   │──►│  (Tools API)    │  │
│  │              │  │              │  │                  │  │
│  │ - Mistral 7B │  │ - Chat UI    │  │ - File access    │  │
│  │ - Llama 3    │  │ - Notes      │  │ - Python exec    │  │
│  │ - Phi-3 Mini │  │ - Knowledge  │  │ - Time/search    │  │
│  └──────────────┘  └──────────────┘  └──────────────────┘  │
│         ▲                                                   │
│         │ Optional                                          │
│  ┌──────┴───────┐                                          │
│  │  TinyProxy   │ ◄── Whitelist-only outbound access       │
│  └──────────────┘                                          │
└─────────────────────────────────────────────────────────────┘
```

### Key Features

**Multi-Model Support**
- Pre-configured with Mistral 7B, Llama 3, and Phi-3 Mini
- Models download automatically on first run and persist across restarts
- Easy to add additional models from Ollama's library

**MCP Tool Integration**
- Custom MCP server exposing tools via OpenAPI/REST
- Sandboxed Python code execution with timeout protection
- File system access within container boundaries
- Seamlessly integrates with Open-webui's tool calling UI

**Production-Ready Configuration**
- Health checks ensure proper startup sequencing
- Persistent volumes for conversations, settings, and model weights
- Backup/restore commands for data portability
- Optional proxy profile for testing true offline capability

**Developer Experience**
- Makefile with common operations (`build-and-run`, `logs`, `backup`, `clean`)
- Python development setup with `uv` package manager
- Agent scaffold for building custom AI workflows
- Comprehensive documentation split into focused guides

## Technical Highlights

### Health Check Implementation

```yaml
ollama:
  healthcheck:
    test: ["CMD-SHELL", "ollama list || exit 1"]
    interval: 30s
    timeout: 10s
    retries: 5
    start_period: 60s

open-webui:
  depends_on:
    ollama:
      condition: service_healthy
```

Open-webui waits for Ollama to be healthy before starting, ensuring models are
available when the UI loads.

### MCP Tool Security

The Python execution tool demonstrates defense-in-depth:

```python
def run_python(code: str) -> str:
    # Block dangerous patterns
    dangerous = ["import os", "import subprocess", "eval(", "exec("]
    for pattern in dangerous:
        if pattern in code:
            return f"Error: '{pattern}' is not allowed"
    
    # Execute in subprocess with timeout
    result = subprocess.run(
        ["python", "-c", code],
        capture_output=True,
        timeout=10,
        env={"PATH": "/usr/bin"}  # Minimal environment
    )
```

### Network Isolation Testing

The optional TinyProxy profile enables verification that models run without
external dependencies:

```bash
# Run with network restrictions
make build-and-run-with-proxy

# Only whitelisted domains accessible
# Models respond = truly local
# Timeouts = external dependency detected
```

## Results

- **Zero-config startup:** Single command brings up entire environment
- **Persistent state:** Conversations and settings survive container restarts
- **Extensible tools:** Add new MCP tools with a simple decorator pattern
- **Documentation-first:** Comprehensive guides for setup, troubleshooting, and development

## Links

- **Source Code:** [GitHub Repository](#)
- **Documentation:** See `/docs` folder for detailed guides
- **Technologies:** Docker, Ollama, Open-webui, MCP, Python, FastAPI

---

*Built as a learning environment for exploring local AI model deployment and
tool integration patterns.*
