"""
Simple AI Agent with MCP Server Integration

This agent demonstrates:
- Connection to local Ollama models
- Tool definition and calling
- MCP server integration (scaffold for Phase 2)
- Structured output handling
"""

import asyncio
import json
from typing import Any, Callable

import httpx
import pydantic
from pydantic import BaseModel, Field


# ============================================================================
# Tool Definitions
# ============================================================================


class Tool(BaseModel):
    """Tool that an agent can call"""

    name: str = Field(description="Name of the tool")
    description: str = Field(description="What this tool does")
    parameters: dict[str, Any] = Field(description="JSON schema for tool parameters")

    def to_dict(self) -> dict:
        return self.model_dump()


class ToolResult(BaseModel):
    """Result from executing a tool"""

    tool_name: str
    success: bool
    result: Any
    error: str | None = None


# ============================================================================
# Simple Tools (Examples for Phase 2)
# ============================================================================


def add_numbers(a: float, b: float) -> float:
    """Add two numbers together"""
    return a + b


def multiply_numbers(a: float, b: float) -> float:
    """Multiply two numbers"""
    return a * b


def get_current_time() -> str:
    """Get the current time"""
    from datetime import datetime
    return datetime.now().isoformat()


# Tool registry - expand this as you add more tools
TOOL_REGISTRY: dict[str, Callable] = {
    "add_numbers": add_numbers,
    "multiply_numbers": multiply_numbers,
    "get_current_time": get_current_time,
}

TOOL_DEFINITIONS: list[Tool] = [
    Tool(
        name="add_numbers",
        description="Add two numbers together",
        parameters={
            "type": "object",
            "properties": {
                "a": {"type": "number", "description": "First number"},
                "b": {"type": "number", "description": "Second number"},
            },
            "required": ["a", "b"],
        },
    ),
    Tool(
        name="multiply_numbers",
        description="Multiply two numbers",
        parameters={
            "type": "object",
            "properties": {
                "a": {"type": "number", "description": "First number"},
                "b": {"type": "number", "description": "Second number"},
            },
            "required": ["a", "b"],
        },
    ),
    Tool(
        name="get_current_time",
        description="Get the current time",
        parameters={"type": "object", "properties": {}, "required": []},
    ),
]


# ============================================================================
# Simple Agent
# ============================================================================


class SimpleAgent:
    """A simple agent that can call Ollama and use tools"""

    def __init__(
        self,
        ollama_host: str = "http://localhost:11434",
        model: str = "mistral",
    ):
        self.ollama_host = ollama_host
        self.model = model
        self.client = httpx.AsyncClient(timeout=30.0)

    async def close(self) -> None:
        """Close the HTTP client"""
        await self.client.aclose()

    async def call_ollama(self, prompt: str) -> str:
        """Call Ollama API and get a response"""
        try:
            response = await self.client.post(
                f"{self.ollama_host}/api/generate",
                json={"model": self.model, "prompt": prompt, "stream": False},
            )
            response.raise_for_status()
            return response.json()["response"]
        except Exception as e:
            return f"Error calling Ollama: {e}"

    def execute_tool(self, tool_name: str, parameters: dict) -> ToolResult:
        """Execute a tool by name with given parameters"""
        if tool_name not in TOOL_REGISTRY:
            return ToolResult(
                tool_name=tool_name,
                success=False,
                result=None,
                error=f"Tool '{tool_name}' not found",
            )

        try:
            tool_func = TOOL_REGISTRY[tool_name]
            result = tool_func(**parameters)
            return ToolResult(tool_name=tool_name, success=True, result=result)
        except Exception as e:
            return ToolResult(
                tool_name=tool_name,
                success=False,
                result=None,
                error=str(e),
            )

    async def run(self, user_message: str) -> str:
        """Run agent with user message and tool calling"""
        print(f"\n📝 User: {user_message}")

        # Build system prompt with available tools
        tools_description = "\n".join(
            [f"- {t.name}: {t.description}" for t in TOOL_DEFINITIONS]
        )
        system_prompt = f"""You are a helpful AI assistant with access to the following tools:

{tools_description}

When the user asks you to do something that requires a tool, respond with a JSON block like this:
{{"thought": "why you need this tool", "tool": "tool_name", "parameters": {{"param1": value1}}}}

Otherwise, just respond naturally."""

        full_prompt = f"{system_prompt}\n\nUser: {user_message}"

        # Get response from Ollama
        response = await self.call_ollama(full_prompt)
        print(f"\n🤖 Ollama: {response}")

        # Try to parse tool call from response
        try:
            # Look for JSON block in response
            import re
            json_match = re.search(r"\{.*\}", response, re.DOTALL)
            if json_match:
                tool_call = json.loads(json_match.group())
                if "tool" in tool_call and "parameters" in tool_call:
                    tool_name = tool_call["tool"]
                    parameters = tool_call["parameters"]
                    print(f"\n🔧 Calling tool: {tool_name} with {parameters}")

                    result = self.execute_tool(tool_name, parameters)
                    print(f"✅ Tool result: {result.result}")
                    return f"Tool '{tool_name}' executed: {result.result}"
        except (json.JSONDecodeError, ValueError):
            pass  # No valid tool call, just return response

        return response


# ============================================================================
# MCP Server Integration (Scaffold for Phase 2)
# ============================================================================

# TODO: Phase 2 - Integrate MCP server
# from mcp.server import Server
# from mcp.types import Tool as MCPTool
#
# async def setup_mcp_server():
#     """Setup MCP server for external tool access"""
#     # This will be implemented in Phase 2
#     # MCP allows your agent to:
#     # - Read files from filesystem
#     # - Make HTTP requests
#     # - Query databases
#     # - Call external APIs with proper sandboxing
#     pass


# ============================================================================
# Main
# ============================================================================


async def main():
    """Example usage of the agent"""
    agent = SimpleAgent(ollama_host="http://localhost:11434", model="mistral")

    try:
        # Example interactions
        result = await agent.run("What is 5 plus 3? Use the add_numbers tool.")
        print(f"\nFinal result: {result}")

        result2 = await agent.run("What time is it?")
        print(f"\nFinal result: {result2}")
    finally:
        await agent.close()


if __name__ == "__main__":
    asyncio.run(main())
