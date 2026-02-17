# API Reference

Quick reference for all active service endpoints and APIs.

## Service URLs

| Service | URL | Purpose |
|---------|-----|---------|
| **Open-webui** | http://localhost:3000 | ChatGPT-style chat interface |
| **Ollama API** | http://localhost:11434 | LLM inference and model management |
| **MCP Server** | http://localhost:8000 | Tool integration and function calling |
| **MCP Swagger UI** | http://localhost:8000/docs | Interactive API documentation |

---

## Open-webui

The main web interface for interacting with LLMs and accessing tools.

```
URL: http://localhost:3000
```

### Authentication

First user to register becomes admin. Set a strong password.

### Features

- Chat with multiple models (Mistral, Llama 3, Phi-3 Mini)
- Conversations persist across sessions
- Integration with MCP tools via function calling
- File uploads and knowledge base management

---

## Ollama API

HTTP API for model inference and management.

```
Base URL: http://localhost:11434
```

### List Available Models

```bash
curl http://localhost:11434/api/tags
```

**Response:**
```json
{
  "models": [
    {
      "name": "mistral:latest",
      "modified_at": "2026-02-05T18:51:23.942Z",
      "size": 7506221056,
      "digest": "...",
      "details": {
        "type": "model",
        "format": "gguf",
        "family": "mistral",
        "families": ["mistral"],
        "parameter_size": "7B",
        "quantization_level": "Q4_0"
      }
    }
  ]
}
```

### Generate Completion

```bash
curl -X POST http://localhost:11434/api/generate \
  -H "Content-Type: application/json" \
  -d '{
    "model": "mistral",
    "prompt": "What is the capital of France?",
    "stream": false
  }'
```

**Parameters:**
- `model` (string): Model name to use
- `prompt` (string): Input prompt
- `stream` (boolean): Return response as stream or single response
- `temperature` (number): 0-1, higher = more creative
- `top_k` (number): Limit tokens to top k
- `top_p` (number): Nucleus sampling parameter

### Chat Completion

```bash
curl -X POST http://localhost:11434/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "model": "mistral",
    "messages": [
      {
        "role": "user",
        "content": "Hello!"
      }
    ],
    "stream": false
  }'
```

**Parameters:**
- `model` (string): Model name
- `messages` (array): Chat message history
  - `role` (string): "user", "assistant", or "system"
  - `content` (string): Message text
- `stream` (boolean): Stream response or return full completion
- `temperature` (number): Sampling temperature (0-1)

### Generate Embeddings

```bash
curl -X POST http://localhost:11434/api/embeddings \
  -H "Content-Type: application/json" \
  -d '{
    "model": "mistral",
    "prompt": "Hello world"
  }'
```

**Response:**
```json
{
  "embeddings": [
    0.01234, 0.05678, -0.12345, ...
  ]
}
```

### Pull a Model

```bash
curl -X POST http://localhost:11434/api/pull \
  -d '{"name": "codellama"}'
```

**Note:** This downloads the model. Check progress with logs:

```bash
docker logs ollama
```

---

## MCP Server (Tool Integration)

OpenAPI-compatible server providing tools for LLM function calling.

```
Base URL: http://localhost:8000
```

### Interactive Documentation

```
http://localhost:8000/docs
```

Opens Swagger UI where you can test all tools directly.

### OpenAPI Specification

```bash
curl http://localhost:8000/openapi.json
```

---

## MCP Tools

All tools are POST endpoints that accept JSON payloads.

### read_file

Read contents of a file in `/data` directory.

```bash
curl -X POST http://localhost:8000/read_file \
  -H "Content-Type: application/json" \
  -d '{
    "filepath": "notes/example.md"
  }'
```

**Parameters:**
- `filepath` (string): Relative path from `/data`

**Returns:** File contents

---

### list_directory

List files and folders in a directory.

```bash
curl -X POST http://localhost:8000/list_directory \
  -H "Content-Type: application/json" \
  -d '{
    "directory": "."
  }'
```

**Parameters:**
- `directory` (string): Path relative to `/data` (default: `.`)

**Returns:** Newline-separated list of files and folders

---

### get_current_time

Get current date and time with timezone support.

```bash
curl -X POST http://localhost:8000/get_current_time \
  -H "Content-Type: application/json" \
  -d '{
    "timezone": "UTC"
  }'
```

**Parameters:**
- `timezone` (string): IANA timezone (e.g., "UTC", "US/Eastern")

**Returns:** ISO 8601 formatted timestamp

---

### run_python

Execute Python code snippets safely (sandboxed).

```bash
curl -X POST http://localhost:8000/run_python \
  -H "Content-Type: application/json" \
  -d '{
    "code": "import json\ndata = {\"x\": 1, \"y\": 2}\nprint(json.dumps(data))"
  }'
```

**Parameters:**
- `code` (string): Python code to execute

**Returns:** stdout and stderr combined

**Restrictions:**
- 10-second timeout
- `os.system`, `subprocess`, `eval`, `exec` blocked
- Working directory limited to `/app`

---

### search_files

Search for files matching a glob pattern.

```bash
curl -X POST http://localhost:8000/search_files \
  -H "Content-Type: application/json" \
  -d '{
    "pattern": "*.md"
  }'
```

**Parameters:**
- `pattern` (string): Glob pattern (e.g., `*.py`, `**/*.md`)

**Returns:** Newline-separated list of matching file paths

---

## Optional: TinyProxy

When proxy profile is enabled (`make build-and-run-with-proxy`).

```
Base URL: http://localhost:8888
```

### Configuration

Whitelist managed in `tinyproxy-whitelist.txt`. Only whitelisted domains are reachable.

### Testing

```bash
curl -x http://localhost:8888:8888 http://example.com
```

If blocked:
```
[CONNECT example.com:443 0] - Establishing SSL tunnel
```

---

## Docker API (Advanced)

Execute commands in containers directly.

### Run command in ollama container

```bash
docker exec ollama ollama list
```

### Run command in mcp-server container

```bash
docker exec mcp-server python -c "print('Hello')"
```

### View container logs

```bash
docker logs ollama      # Last 100 lines
docker logs -f ollama   # Follow (tail -f)
docker logs --tail 50 ollama  # Last 50 lines
```

---

## Test Commands

### Test Ollama

```bash
# List models
curl http://localhost:11434/api/tags

# Quick generation
curl -X POST http://localhost:11434/api/generate \
  -H "Content-Type: application/json" \
  -d '{"model":"mistral","prompt":"hi","stream":false}'
```

### Test MCP Server

```bash
# Get current time
curl -X POST http://localhost:8000/get_current_time

# List data directory
curl -X POST http://localhost:8000/list_directory \
  -H "Content-Type: application/json" \
  -d '{"directory":"."}'

# Run simple Python
curl -X POST http://localhost:8000/run_python \
  -H "Content-Type: application/json" \
  -d '{"code":"print(2+2)"}'
```

### Test Open-webui

Visit http://localhost:3000 in browser. Should load chat interface.

---

## Troubleshooting

### Service not responding

```bash
# Check if container is running
docker ps | grep <service>

# Check container health
docker ps --format "table {{.Names}}\t{{.Status}}"

# View recent logs
docker logs <container> --tail 50
```

### MCP tools not showing in Open-webui

1. Verify MCP server is running:
   ```bash
   curl http://localhost:8000/docs
   ```

2. Add in Open-webui: **Settings → Tools** → Add `http://localhost:8000`

3. Enable tools in chat with the **+** button at bottom left

### Connection refused errors

May indicate port binding issue or container not started:

```bash
# Restart all containers
make stop
make build-and-run

# Check ports
netstat -tuln | grep -E "(3000|8000|11434)"
```
