from mcp_client import BrightDataMCP

mcp = BrightDataMCP()
result = mcp.search_engine(
    query="E-commerce startup funding news site:techcrunch.com"
)

print("FULL RAW MCP RESULT:\n")
print(result)
