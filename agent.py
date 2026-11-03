# Εδώ ορίζεται ο AI Agent κι εκτελείται ως subprocess σε συγκεκριμένο port.
import asyncio
import json
import httpx
import sys

from fastmcp import FastMCP
from flask import Flask, request, jsonify
from langchain.mcp import MCPAdapter
from langgraph.prebuilt import create_react_agent
from langchain_core.tools import StructuredTool
from langchain_ollama import ChatOllama
from playwright.async_api import async_playwright
from typing import Any

from crud.repos.MCPServersRepository import MCPServersRepository
from crud.repos.RestAPIsRepository import RestAPIsRepository
from crud.repos.WebsitesRepository import WebsitesRepository

global payload
global model
global tools
global agent

tools = []

rest_apis_repo = RestAPIsRepository()
mcp_servers_repo = MCPServersRepository()
websites_repo = WebsitesRepository()

# Συνάρτηση για την απόκτηση εργαλείων από το OpenAPI spec μέσω του MCP server.
async def add_tools_from_api(data: dict):
    domain = data.get("domain")
    openapi_spec = data.get("openapi_spec")
    mcp_server_name = data.get("mcp_server_name")

    http_client = httpx.AsyncClient(base_url=domain)

    openapi_spec_json = httpx.get(domain + openapi_spec).json()

    # Δημιουργία FastMCP server από το OpenAPI spec.
    mcp_server = FastMCP.from_openapi(
        name=mcp_server_name,
        client=http_client,
        openapi_spec=openapi_spec_json
    )

    # Με τη βοήθεια του Adapter μετατρέπουμε αυτόματα τα εργαλεία του MCP Server σε εργαλεία συμβατά με το LangChain.
    langchain_tools = []
    async with MCPAdapter(mcp_server) as adapter:
        langchain_tools = await adapter.list_tools()

    tools.extend(langchain_tools)

# Συνάρτηση για την απόκτηση εργαλείων από Website με WebMCP standard.
async def add_tools_from_website(data: dict):
    # Συνάρτηση για τη δημιουργία δυναμικού εργαλείου από Website.
    def create_tool(domain: str, tool_name: str):
        async def dynamic_tool(**kwargs) -> Any:
            async with async_playwright() as p:
                # Ανοίγουμε τον browser.
                browser = await p.chromium.launch(
                    headless=True,
                    args=[
                        "--enable-features=WebMCP",
                        "--no-sandbox",
                        "--disable-setuid-sandbox",
                        "--disable-dev-shm-usage"
                    ]
                )

                # Πλοηγούμαστε στην αρχική σελίδα του website.
                page = await browser.new_page()
                await page.goto(domain)

                # Καλούμε το WebMCP εργαλείο.
                result = await page.webmcp.call_tool(name=tool_name, input=kwargs)

                # Κλείνουμε τον browser.
                await browser.close()

                return result
        
        dynamic_tool.__name__ = tool_name
        return dynamic_tool

    domain = data.get("domain")

    pure_langchain_tools = []

    async with async_playwright() as p:
        # Ανοίγουμε τον browser.
        browser = await p.chromium.launch(
            headless=True,
            args=[
                "--enable-features=WebMCP",
                "--no-sandbox",
                "--disable-setuid-sandbox",
                "--disable-dev-shm-usage"
            ]
        )

        # Πλοηγούμαστε στην αρχική σελίδα του website.
        page = await browser.new_page()
        await page.goto(domain) 

        # Διαβάζουμε τα διαθέσιμα WebMCP εργαλεία.
        web_tools = await page.webmcp.tools()
        
        if not web_tools:
            await browser.close()
            return

        for tool in web_tools:
            # Τα απαραίτητα properties του WebMCP εργαλείου που χρειαζόμαστε.
            tool_name = tool['name']
            tool_desc = tool['description']
            input_schema = tool.get("inputSchema", {"type": "object", "properties": {}})

            # Δημιουργούμε τη δυναμική συνάρτηση για το εργαλείο.
            func = create_tool(domain, tool_name)

            # Δημιουργούμε το LangChain εργαλείο από τη δυναμική συνάρτηση.
            lc_tool = StructuredTool.from_function(
                coroutine=func,
                name=tool_name,
                description=tool_desc,
                args_schema=input_schema
            )
            
            pure_langchain_tools.append(lc_tool)

        # Κλείνουμε τον browser.
        await browser.close()

        tools.extend(pure_langchain_tools)

# Κατά την εκκίνηση του agent ελέγχουμε αν μας δόθηκε το payload.
if len(sys.argv) < 2:
    print("Σφάλμα: Δεν δόθηκε payload στον Agent.")
    sys.exit(1)

try:
    # Το sys.argv[0] είναι το όνομα του αρχείου (agent.py).
    # Το sys.argv[1] είναι το JSON string που στείλαμε.
    raw_payload = sys.argv[1]
    
    # Μετατροπή του JSON string σε dictionary.
    payload = json.loads(raw_payload)
    
except json.JSONDecodeError:
    print("Σφάλμα: Το payload δεν ήταν έγκυρο JSON.")
    sys.exit(1)

# Αρχικοποίηση του LLM.
model = ChatOllama(
    model=payload.get("llm"), 
    base_url="http://ollama:11434"
)

# Λίστα με τα IDs των MCP servers που θα χρησιμοποιηθούν από το payload.
mcp_server_ids = payload.get("mcp_server_ids", [])

# Ανάκτηση των MCP servers από το payload.
mcp_servers = []
for server_id in mcp_server_ids:
    mcp_server = mcp_servers_repo.get_by_id(server_id)
    if mcp_server:
        mcp_servers.append(mcp_server)

# Για κάθε MCP Server με βάση το πεδίο 'type' βρίσκουμε τα συσχετιζόμενα εργαλεία.
for mcp_server in mcp_servers:
    mcp_server_name = mcp_server.get("name")

    if mcp_server.get("type") == "Rest API": # 1η περίπτωση: Rest API MCP server.
        rest_api = rest_apis_repo.get_by_id(mcp_server.get("restapi_id"))
        if not rest_api:
            continue

        openapi_spec = rest_api.get("openapi_spec")
        domain = rest_api.get("domain")

        if mcp_server_name and openapi_spec and domain:
            data = {
                "domain": domain,
                "openapi_spec": openapi_spec,
                "mcp_server_name": mcp_server_name
            }
            asyncio.run(add_tools_from_api(data))
    elif mcp_server.get("type") == "Website": # 2η περίπτωση: Website MCP server.
        website = websites_repo.get_by_id(mcp_server.get("website_id"))
        if not website:
            continue

        domain = website.get("domain")

        if domain:
            data = {
                "domain": domain
            }
            asyncio.run(add_tools_from_website(data))

# Δημιουργούμε τον AI Agent.
agent = create_react_agent(model=model, prompt=payload.get("system_prompt"), tools=tools)

# Κλήση του AI Agent με το μήνυμα του χρήστη.
async def call(user_message: str):
    response = await agent.ainvoke({"messages": [{"role": "user", "content": user_message}]})
    return response["messages"][-1].content

# Ο Flask server για την επικοινωνία με τον χρήστη.
app = Flask(__name__)

# Η κλήση του Flask endpoint για την επικοινωνία με τον AI Agent.
@app.route("/chat", methods=["POST"])
def run_agent():
    try:
        data = request.get_json()
        if not data or 'message' not in data:
            return jsonify({"error": "Missing 'message' in request body"}), 400
        
        user_message = data['message']

        # Για το συγκεκριμένο thread του request δημιουργούμε ή ανακτούμε το event loop.
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
        # Καλούμε τον AI Agent με το μήνυμα του χρήστη.
        output_text = loop.run_until_complete(call(user_message))

        return jsonify({
            "status": "success",
            "output": output_text
        })
    except Exception as e:
        return jsonify({"error": "Δυστυχώς προέκυψε σφάλμα κατά την εκτέλεση της διεργασίας."}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=payload.get("port"), debug=False)