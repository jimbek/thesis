import asyncio
import json
import requests
import sys

from flask import Flask, request, jsonify
from fastmcp import FastMCP
from langchain_ollama import ChatOllama
from langchain.mcp import MCPAdapter
from langgraph.prebuilt import create_react_agent

from crud.repos.RestAPIsRepository import RestAPIsRepository
from crud.repos.MCPServersRepository import MCPServersRepository

global payload
global model
global tools
global agent

tools = []

rest_apis_repo = RestAPIsRepository()
mcp_servers_repo = MCPServersRepository()

# Συνάρτηση για την απόκτηση εργαλείων από το OpenAPI spec μέσω του MCP server.
async def add_tools_from_api(data: dict):
    domain = data.get("domain")
    openapi_spec = data.get("openapi_spec")
    mcp_server_name = data.get("mcp_server_name")

    mcp_server = FastMCP(mcp_server_name)

    try:
        response = requests.get(domain + openapi_spec, timeout=10)
        schema = response.json()
        paths = schema.get("paths", {})
    except Exception as e:
        paths = {}
        
    for path, methods in paths.items():
        for method, details in methods.items():
            if method.lower() not in ["get", "post", "put", "delete"]:
                continue

            operation_id = details.get("operationId")
            summary = details.get("summary", f"Κλήση του {method.upper()} {path}")
            
            if not operation_id:
                operation_id = f"{method}_{path.replace('/', '_').strip('_')}"
            
            operation_id = operation_id.replace("-", "_").replace(".", "_")

            def make_api_call(target_path=path, target_method=method):
                def dynamic_tool(query: str = ""):
                    url = f"{domain}{target_path}"
                    params = {"q": query} if query else {}
                    
                    if target_method.lower() == "get":
                        res = requests.get(url, params=params, timeout=10)
                    elif target_method.lower() == "post":
                        res = requests.post(url, json=params, timeout=10)
                    elif target_method.lower() == "put":
                        res = requests.put(url, json=params, timeout=10)
                    elif target_method.lower() == "delete":
                        res = requests.delete(url, json=params, timeout=10)
                    else:
                        return f"Unsupported method: {target_method}"
                        
                    return res.json() if res.status_code == 200 else f"Error {res.status_code}: {res.text}"
                return dynamic_tool

            tool_func = make_api_call()
            tool_func.__name__ = operation_id
            tool_func.__doc__ = f"{summary}\n\nPath: {path}\nMethod: {method.upper()}"
            
            mcp_server.tool()(tool_func)

    mcp_tools = []

    async with MCPAdapter(mcp_server) as adapter:
        mcp_tools = await adapter.list_tools()

    tools.extend(mcp_tools)

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
    if mcp_server.get("type") == "Rest API":
        rest_api = rest_apis_repo.get_by_id(mcp_server.get("restapi_id"))
        if not rest_api:
            continue

        mcp_server_name = mcp_server.get("name")
        openapi_spec = rest_api.get("openapi_spec")
        domain = rest_api.get("domain")

        if mcp_server_name and openapi_spec and domain:
            data = {
                "domain": domain,
                "openapi_spec": openapi_spec,
                "mcp_server_name": mcp_server_name
            }
            asyncio.run(add_tools_from_api(data))

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