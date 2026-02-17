# Python Development

This project uses `uv` as the Python package manager. All dependencies are
defined in `pyproject.toml` targeting Python 3.11+.

## Setup

### Install uv

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Install project dependencies

```bash
make py-setup
```

Or manually:

```bash
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv sync
```

## Running Scripts

### Agent script

The `src/agent.py` file provides a scaffold for building an AI agent with:

- Direct Ollama API integration
- Tool definition and execution framework
- Structured output handling with Pydantic

```bash
make py-agent
```

Or manually:

```bash
uv run src/agent.py
```

### Direct model interaction

The `src/chat_mistral.py` script demonstrates direct model interaction using
HuggingFace Transformers (requires GPU and significant RAM):

```bash
uv run src/chat_mistral.py
```

## Project Structure

| File                      | Description                                    |
| ------------------------- | ---------------------------------------------- |
| `pyproject.toml`          | Python project configuration and dependencies  |
| `src/agent.py`            | AI agent scaffold with tool calling            |
| `src/chat_mistral.py`     | Direct HuggingFace Transformers interaction    |
| `src/mcp_server.py`       | MCP server implementation                      |

## Adding Dependencies

Add new dependencies to `pyproject.toml`:

```toml
[project]
dependencies = [
    "httpx>=0.27.0",
    "pydantic>=2.0",
    "your-new-package>=1.0",  # Add here
]
```

Then sync:

```bash
uv sync
```

## Development Commands

```bash
make py-setup    # Create venv and install dependencies
make py-agent    # Run the agent script
make py-lint     # Run linting (if configured)
make py-test     # Run tests (if configured)
```
