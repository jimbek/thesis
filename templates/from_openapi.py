import requests
from flask import Flask, request, jsonify
from fastmcp import FastMCP
from langchain_ollama import ChatOllama
from langchain.mcp import MCPAdapter
from langgraph.prebuilt import create_react_agent

# Αρχικοποίηση MCP Server.
mcp_server = FastMCP("EDYP MCP Server")

SWAGGER_URL = "/v3/api-docs"
BASE_API_URL = "https://edyp.gr"

def from_api():
    try:
        response = requests.get(BASE_API_URL + SWAGGER_URL, timeout=10)
        schema = response.json()
        paths = schema.get("paths", {})
    except Exception as e:
        paths = {}
        
    for path, methods in paths.items():
        for method, details in methods.items():
            if method.lower() not in ["get", "post"]:
                continue

            operation_id = details.get("operationId")
            summary = details.get("summary", f"Κλήση του {method.upper()} {path}")
            
            if not operation_id:
                operation_id = f"{method}_{path.replace('/', '_').strip('_')}"
            
            operation_id = operation_id.replace("-", "_").replace(".", "_")

            def make_api_call(target_path=path, target_method=method):
                def dynamic_tool(query: str = ""):
                    url = f"{BASE_API_URL}{target_path}"
                    params = {"q": query} if query else {}
                    
                    if target_method.lower() == "get":
                        res = requests.get(url, params=params, timeout=10)
                    else:
                        res = requests.post(url, json=params, timeout=10)
                        
                    return res.json() if res.status_code == 200 else f"Error {res.status_code}: {res.text}"
                return dynamic_tool

            tool_func = make_api_call()
            tool_func.__name__ = operation_id
            tool_func.__doc__ = f"{summary}\n\nPath: {path}\nMethod: {method.upper()}"
            
            mcp_server.tool()(tool_func)

# Εκτέλεση του from_api() κατά την εκκίνηση του αρχείου.
from_api()

# Κλήση του AI Agent με το μήνυμα του χρήστη.
async def call(user_message: str):
    model = ChatOllama(
        model="llama3.2", 
        base_url="http://localhost:11434"
    )

    async with MCPAdapter(mcp_server) as adapter:
        mcp_tools = await adapter.list_tools()
        agent = create_react_agent(model=model, tools=mcp_tools)

        response = await agent.ainvoke({"messages": [{"role": "user", "content": user_message}]})
        return response["messages"][-1].content


# Ο Flask server για την επικοινωνία με τον χρήστη.
app = Flask(__name__)

@app.route("/chat", methods=["POST"])
async def run_agent():
    data = request.get_json()
    if not data or 'message' not in data:
        return jsonify({"error": "Missing 'message' in request body"}), 400
    
    user_message = data['message']

    try:
        output_text = await call(user_message)
        return jsonify({
            "status": "success",
            "output": output_text
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8001, debug=False)