from mcp_client import BrightDataMCP
from agents.company_discovery import create_company_discovery_agent
from bs4 import BeautifulSoup

print("🟦 Testing MCP + Company Discovery Workflow")

# --------------------------------------------------
# 1. Initialize MCP client
# --------------------------------------------------
mcp = BrightDataMCP()
print("MCP Ready:", mcp is not None)

# --------------------------------------------------
# 2. Create company discovery agent
# --------------------------------------------------
agent = create_company_discovery_agent(mcp)

# --------------------------------------------------
# 3. Test discovery tool
# --------------------------------------------------
print("\n🔍 Running company search: SaaS startup\n")

try:
    results = agent.tools[0]._run("SaaS", "startup", "USA")
    print("📊 Parsed Company Results:")
    print(results)
except Exception as e:
    print("❌ Error during discovery:", str(e))


# --------------------------------------------------
# 4. RAW MCP result + FIXED parser
# --------------------------------------------------
print("\n🟪 RAW MCP TEST (search_engine)\n")

query = "E-commerce startup funding news site:techcrunch.com"

try:
    raw = mcp.tools["search_engine"](query=query)
    print("Raw result type:", type(raw))
    print("Raw keys:", raw.keys() if isinstance(raw, dict) else None)

    # --------------------------------------------------
    # FIX START: BrightData MCP returns { response: "<html>..." }
    # --------------------------------------------------
    if isinstance(raw, dict) and "response" in raw:
        html = raw["response"]
        print(f"\nHTML Length: {len(html)} characters")

        soup = BeautifulSoup(html, "html.parser")

        # Extract searchable data
        items = []
        for a in soup.find_all("a"):
            title = a.get_text(strip=True)
            link = a.get("href")
            if title and link and link.startswith("http"):
                items.append({"title": title, "link": link})

        if items:
            print(f"\n🔎 Extracted {len(items)} search results:")
            for i, item in enumerate(items[:5], start=1):
                print(f"\nResult {i}")
                print("TITLE:", item["title"])
                print("LINK:", item["link"])
        else:
            print("⚠ No extractable titles/links from HTML")

    else:
        print("⚠ MCP returned no HTML response")

except Exception as e:
    print("❌ MCP call failed:", str(e))
