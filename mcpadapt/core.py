import asyncio
from contextlib import asynccontextmanager
import os

from mcp.client.session import ClientSession
from mcp.client.stdio import StdioServerParameters, stdio_client


class MCPAdapt:
    """MCP Adapter that runs a Node MCP server over stdio."""

    def __init__(self, server_params, adapter=None):
        if not isinstance(server_params, StdioServerParameters):
            raise TypeError(
                f"server_params must be StdioServerParameters, got {type(server_params)}"
            )

        self.server_params = server_params
        self.adapter = adapter
        self.loop = asyncio.new_event_loop()

    @asynccontextmanager
    async def connect(self):
        """Start MCP server via stdio_client() correctly."""
        print(f"[MCPAdapt] Using server params: {self.server_params}")

        # Merge environment variables
        merged_env = os.environ.copy()
        merged_env.update(self.server_params.env)
        self.server_params.env = merged_env

        # CORRECT stdio_client CALL
        async with stdio_client(self.server_params) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                yield session

    async def run(self):
        """List active MCP tools."""
        async with self.connect() as session:
            result = await session.list_tools()
            return result.model_dump()

    async def run_tool(self, name, arguments):
        """Execute a single MCP tool."""
        async with self.connect() as session:
            result = await session.call_tool(name, arguments)
            return result.model_dump()

    def __enter__(self):
        self._tools = self.loop.run_until_complete(self.run())
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass

    def __iter__(self):
        for tool in self._tools.get("tools", []):
            yield ToolWrapper(self, tool)


class ToolWrapper:
    """Wrapper to call MCP tools synchronously."""
    def __init__(self, adapter, tool_info):
        self.adapter = adapter
        self.name = tool_info.get("name")
        self.description = tool_info.get("description")

    def run(self, **arguments):
        return self.adapter.loop.run_until_complete(
            self.adapter.run_tool(self.name, arguments)
        )
