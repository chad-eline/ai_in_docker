#!/usr/bin/env python3
"""
MCP Server for Open-webui Integration

This server provides tools that can be called by LLMs through Open-webui.
It uses stdio transport and is meant to be proxied through MCPO.

Tools provided:
- read_file: Read contents of a file
- list_directory: List files in a directory
- get_current_time: Get current date and time
- run_python: Execute Python code snippets (sandboxed)
- search_files: Search for files by pattern
"""

import asyncio
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import TextContent, Tool

# Configuration
ALLOWED_DIRECTORIES = [
    "/data",  # Mounted data directory
    "/tmp",   # Temporary files
]
MAX_FILE_SIZE = 1024 * 1024  # 1MB max file read
PYTHON_TIMEOUT = 10  # seconds


def is_path_allowed(path: str) -> bool:
    """Check if a path is within allowed directories."""
    try:
        resolved = Path(path).resolve()
        return any(
            str(resolved).startswith(allowed)
            for allowed in ALLOWED_DIRECTORIES
        )
    except Exception:
        return False


def safe_read_file(path: str, max_lines: int | None = None) -> str:
    """Safely read a file with size limits."""
    if not is_path_allowed(path):
        return f"Error: Access denied. Path must be within: {ALLOWED_DIRECTORIES}"
    
    try:
        file_path = Path(path)
        if not file_path.exists():
            return f"Error: File not found: {path}"
        if not file_path.is_file():
            return f"Error: Not a file: {path}"
        if file_path.stat().st_size > MAX_FILE_SIZE:
            return f"Error: File too large (max {MAX_FILE_SIZE} bytes)"
        
        content = file_path.read_text(encoding="utf-8", errors="replace")
        
        if max_lines:
            lines = content.splitlines()
            if len(lines) > max_lines:
                content = "\n".join(lines[:max_lines])
                content += f"\n... ({len(lines) - max_lines} more lines truncated)"
        
        return content
    except PermissionError:
        return f"Error: Permission denied: {path}"
    except Exception as e:
        return f"Error reading file: {e}"


def safe_list_directory(path: str) -> str:
    """Safely list directory contents."""
    if not is_path_allowed(path):
        return f"Error: Access denied. Path must be within: {ALLOWED_DIRECTORIES}"
    
    try:
        dir_path = Path(path)
        if not dir_path.exists():
            return f"Error: Directory not found: {path}"
        if not dir_path.is_dir():
            return f"Error: Not a directory: {path}"
        
        entries = []
        for entry in sorted(dir_path.iterdir()):
            if entry.is_dir():
                entries.append(f"📁 {entry.name}/")
            else:
                size = entry.stat().st_size
                entries.append(f"📄 {entry.name} ({size} bytes)")
        
        if not entries:
            return f"Directory is empty: {path}"
        
        return f"Contents of {path}:\n" + "\n".join(entries)
    except PermissionError:
        return f"Error: Permission denied: {path}"
    except Exception as e:
        return f"Error listing directory: {e}"


def run_python_sandboxed(code: str) -> str:
    """Run Python code in a subprocess with restrictions."""
    # Basic code safety checks
    dangerous_imports = ["os.system", "subprocess", "eval", "exec", "__import__"]
    for dangerous in dangerous_imports:
        if dangerous in code:
            return f"Error: Potentially dangerous code detected ({dangerous})"
    
    try:
        result = subprocess.run(
            [sys.executable, "-c", code],
            capture_output=True,
            text=True,
            timeout=PYTHON_TIMEOUT,
            env={
                "PATH": "/usr/bin:/bin",
                "PYTHONDONTWRITEBYTECODE": "1",
            },
            cwd="/tmp",
        )
        
        output = ""
        if result.stdout:
            output += result.stdout
        if result.stderr:
            output += f"\nStderr:\n{result.stderr}"
        if result.returncode != 0:
            output += f"\nExit code: {result.returncode}"
        
        return output.strip() or "(No output)"
    
    except subprocess.TimeoutExpired:
        return f"Error: Code execution timed out ({PYTHON_TIMEOUT}s limit)"
    except Exception as e:
        return f"Error executing code: {e}"


def search_files(directory: str, pattern: str) -> str:
    """Search for files matching a pattern in a directory."""
    if not is_path_allowed(directory):
        return f"Error: Access denied. Path must be within: {ALLOWED_DIRECTORIES}"
    
    try:
        dir_path = Path(directory)
        if not dir_path.exists():
            return f"Error: Directory not found: {directory}"
        
        matches = list(dir_path.rglob(pattern))[:50]  # Limit results
        
        if not matches:
            return f"No files found matching '{pattern}' in {directory}"
        
        results = [str(m.relative_to(dir_path)) for m in matches]
        return f"Found {len(matches)} file(s) matching '{pattern}':\n" + "\n".join(results)
    
    except Exception as e:
        return f"Error searching files: {e}"


# Create the MCP server
server = Server("open-webui-tools")


@server.list_tools()
async def list_tools() -> list[Tool]:
    """Return the list of available tools."""
    return [
        Tool(
            name="read_file",
            description="Read the contents of a file. Use this to examine file contents within the /data directory.",
            inputSchema={
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "The absolute path to the file to read (must be in /data or /tmp)",
                    },
                    "max_lines": {
                        "type": "integer",
                        "description": "Maximum number of lines to return (optional, returns all if not specified)",
                    },
                },
                "required": ["path"],
            },
        ),
        Tool(
            name="list_directory",
            description="List the contents of a directory. Use this to explore files and folders within the /data directory.",
            inputSchema={
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "The absolute path to the directory to list (must be in /data or /tmp)",
                    },
                },
                "required": ["path"],
            },
        ),
        Tool(
            name="get_current_time",
            description="Get the current date and time. Useful for time-sensitive queries or logging.",
            inputSchema={
                "type": "object",
                "properties": {
                    "timezone": {
                        "type": "string",
                        "description": "Timezone name (e.g., 'America/New_York'). Defaults to UTC.",
                    },
                },
                "required": [],
            },
        ),
        Tool(
            name="run_python",
            description="Execute a Python code snippet and return the output. Use for calculations, data processing, or quick scripts. Code runs in a sandboxed environment with a 10-second timeout.",
            inputSchema={
                "type": "object",
                "properties": {
                    "code": {
                        "type": "string",
                        "description": "The Python code to execute. Print statements will show in the output.",
                    },
                },
                "required": ["code"],
            },
        ),
        Tool(
            name="search_files",
            description="Search for files matching a glob pattern within a directory. Use this to find files by name or extension.",
            inputSchema={
                "type": "object",
                "properties": {
                    "directory": {
                        "type": "string",
                        "description": "The directory to search in (must be in /data or /tmp)",
                    },
                    "pattern": {
                        "type": "string",
                        "description": "Glob pattern to match (e.g., '*.txt', '**/*.py', 'report*')",
                    },
                },
                "required": ["directory", "pattern"],
            },
        ),
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict[str, Any]) -> list[TextContent]:
    """Handle tool calls."""
    
    if name == "read_file":
        path = arguments.get("path", "")
        max_lines = arguments.get("max_lines")
        result = safe_read_file(path, max_lines)
        
    elif name == "list_directory":
        path = arguments.get("path", "")
        result = safe_list_directory(path)
        
    elif name == "get_current_time":
        tz_name = arguments.get("timezone", "UTC")
        try:
            from zoneinfo import ZoneInfo
            tz = ZoneInfo(tz_name)
            now = datetime.now(tz)
            result = f"Current time ({tz_name}): {now.strftime('%Y-%m-%d %H:%M:%S %Z')}"
        except Exception:
            now = datetime.utcnow()
            result = f"Current time (UTC): {now.strftime('%Y-%m-%d %H:%M:%S')} UTC"
            
    elif name == "run_python":
        code = arguments.get("code", "")
        result = run_python_sandboxed(code)
        
    elif name == "search_files":
        directory = arguments.get("directory", "")
        pattern = arguments.get("pattern", "*")
        result = search_files(directory, pattern)
        
    else:
        result = f"Unknown tool: {name}"
    
    return [TextContent(type="text", text=result)]


async def main():
    """Run the MCP server using stdio transport."""
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options(),
        )


if __name__ == "__main__":
    asyncio.run(main())
