# MCP Server Integration

This project includes an MCP (Model Context Protocol) server that provides tools
to the LLM through Open-webui. The MCP server runs via MCPO proxy, which exposes
the tools as REST/OpenAPI endpoints.

## Available Tools

| Tool             | Description                                          |
| ---------------- | ---------------------------------------------------- |
| `read_file`      | Read contents of files in the `/data` directory      |
| `list_directory` | List files and folders in the `/data` directory      |
| `get_current_time` | Get current date/time with timezone support        |
| `run_python`     | Execute Python code snippets (sandboxed, 10s timeout)|
| `search_files`   | Search for files matching a glob pattern             |

## Setup (One-Time)

### 1. Start the containers

```bash
make build-and-run
```

### 2. Verify MCP server is running

```bash
make mcp-test
```

Or visit the API docs: http://localhost:8000/docs

### 3. Add MCP Server to Open-webui

1. Click your **profile icon** (top right) → **Settings**
2. Go to **Tools** tab
3. Click **+ Add Connection**
4. Configure:
   - **URL:** `http://localhost:8000`
   - **Type:** OpenAPI
   - **Auth:** None
5. Click **Save**

## Using Tools in Chat

### Enable tools per-chat

1. Start a new chat in Open-webui
2. Click the **+** icon in the message input area (bottom left)
3. Toggle ON the tools you want to use

### Example prompts

- "What time is it?"
- "List the files in the data directory"
- "Calculate the sum of 1 to 100 using Python"
- "Read the contents of config.json"

## Custom Models with Pre-enabled Tools

By default, tools must be enabled manually for each chat. To have tools always
enabled, create a Custom Model:

1. Go to **Workspace** → **Models**
2. Click **+ Create a Model**
3. Configure:
   - **Name:** e.g., "Mistral + Tools"
   - **Base Model:** Select `mistral:latest` (or another model)
4. Scroll down to the **Tools** section
5. Toggle ON the MCP tools you want enabled by default
6. Click **Save**

Now when you select "Mistral + Tools" in a chat, all configured tools are
automatically available without needing to enable them manually.

## MCP Server Commands

```bash
make logs-mcp      # View MCP server logs
make mcp-restart   # Restart MCP server after code changes
make mcp-test      # Test MCP server and list available tools
make mcp-docs      # Open MCP API documentation
```

## Using the Data Directory

The MCP tools have access to the `/data` directory inside the container, which
is persisted via Docker volume.

### Copy files to the container

```bash
docker cp myfile.txt mcp-server:/data/
```

### Mount a local directory

Modify `docker-compose.yml` to mount a local folder:

```yaml
mcp-server:
  volumes:
    - mcp_data:/data
    - ./my-local-folder:/data/shared  # Add this line
```

## Security Considerations

### Sandboxed execution

The `run_python` tool runs in a restricted subprocess with:

- 10-second timeout
- Limited environment variables
- Dangerous imports blocked (`os.system`, `subprocess`, `eval`, `exec`)

### Path restrictions

File tools only access `/data` and `/tmp` directories.

### Container isolation

MCP server runs in its own container with minimal privileges.

## Adding Custom Tools

To add new tools, edit `src/mcp_server.py`:

```python
@mcp.tool()
def my_custom_tool(param: str) -> str:
    """Description of what this tool does."""
    # Your implementation here
    return result
```

Then restart the MCP server:

```bash
make mcp-restart
```

The new tool will automatically appear in Open-webui after refreshing.
