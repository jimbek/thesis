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
from playwright.sync_api import sync_playwright

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

    mcp_server = FastMCP.from_openapi(
        name=mcp_server_name,
        client=http_client,
        openapi_spec=openapi_spec_json
    )

    langchain_tools = []
    async with MCPAdapter(mcp_server) as adapter:
        langchain_tools = await adapter.list_tools()

    tools.extend(langchain_tools)

# Συνάρτηση για την απόκτηση εργαλείων από Website με WebMCP standart.
async def add_tools_from_website(data: dict):
    domain = data.get("domain")

    pure_langchain_tools = []

    async with async_playwright() as p:
        browser = await p.chromium.launch(channel="msedge")
        page = await browser.new_page()
        
        await page.goto(domain) 
        await page.wait_for_load_state("networkidle")

        web_tools = await page.evaluate("""
            async () => {
                if (!document.modelContext) return [];
                const rawTools = await document.modelContext.getTools();
                return rawTools.map(t => ({
                    name: t.name,
                    description: t.description
                }));
            }
        """)
        
        if not web_tools:
            await browser.close()
            return

        for tool in web_tools:
            tool_name = tool['name']
            tool_desc = tool['description']

            def make_browser_call(t_name=tool_name):
                def execute_in_page(query: str = ""):
                    with sync_playwright() as playwright:
                        web_browser = playwright.chromium.launch(channel="msedge")
                        web_page = web_browser.new_page()

                        tool_args = {"query": query} if query else {}

                        result_json = web_page.evaluate("""
                            async ([name, args]) => {
                                try {
                                    const res = await document.modelContext.executeTool(name, args);
                                    return JSON.stringify(res);
                                } catch (err) {
                                    return JSON.stringify({ error: err.message });
                                }
                            }
                        """, [t_name, tool_args])

                        web_browser.close()
                    
                    return result_json
                return execute_in_page

            lc_tool = StructuredTool.from_function(
                name=tool_name,
                description=tool_desc,
                func=make_browser_call(tool_name)
            )
            pure_langchain_tools.append(lc_tool)

        await browser.close()

        tools.extend(pure_langchain_tools)

# Κατά την εκκίνηση του agent ελέγχουμε αν μας δόθηκε το payload
if len(sys.argv) < 2:
    print("Σφάλμα: Δεν δόθηκε payload στον Agent.")
    sys.exit(1)

try:
    # Το sys.argv[0] είναι το όνομα του αρχείου (agent.py)
    # Το sys.argv[1] είναι το JSON string που στείλαμε
    raw_payload = sys.argv[1]
    
    # Μετατροπή του JSON string ξανά σε Python dict
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

    if mcp_server.get("type") == "Rest API":
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
    elif mcp_server.get("type") == "Website":
        website = websites_repo.get_by_id(mcp_server.get("website_id"))
        if not website:
            continue

        domain = website.get("domain")

        if domain:
            data = {
                "domain": domain
            }
            asyncio.run(add_tools_from_website(data))

# Αφού έχουμε προσθέσει όλα τα εργαλεία από τα Rest APIs, μπορούμε να συνεχίσουμε με την εκκίνηση του agent.
agent = create_react_agent(model=model, prompt=payload.get("system_prompt"), tools=tools)

# Κλήση του AI Agent με το μήνυμα του χρήστη.
async def call(user_message: str):
    response = await agent.ainvoke({"messages": [{"role": "user", "content": user_message}]})
    return response["messages"][-1].content

# Ο Flask server για την επικοινωνία με τον χρήστη.
app = Flask(__name__)

@app.route("/chat", methods=["POST"])
def run_agent():
    try:
        data = request.get_json()
        if not data or 'message' not in data:
            return jsonify({"error": "Missing 'message' in request body"}), 400
        
        user_message = data['message']

        # Δημιουργία/Ανάκτηση απομονωμένου loop για το συγκεκριμένο thread του request
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
        # Εκτέλεση του async Agent
        output_text = loop.run_until_complete(call(user_message))

        return jsonify({
            "status": "success",
            "output": output_text
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=payload.get("port"), debug=False)