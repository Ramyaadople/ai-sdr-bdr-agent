import asyncio
from mcp_client import BrightDataMCP

async def main():
    print("Initializing MCP...")
    mcp = BrightDataMCP()
    print("✅ BrightData MCP client initialized")

    print("\nCalling MCP tool: search_engine...\n")

    # IMPORTANT — use the MCP client's async call
    raw = await mcp.client.call_tool(
        "search_engine",
        {
            "query": "E-commerce startup funding news site:techcrunch.com",
            "engine": "google"
        }
    )

    print("\n======= FULL RAW MCP RESULT =======\n")
    print(raw)


# Run async
asyncio.run(main())
