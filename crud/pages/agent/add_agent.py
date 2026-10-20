# This page allows the user to add a new AI Agent.
from crud.services.AgentsService import AgentsService
from crud.services.MCPServersService import MCPServersService
from crud.services.LLMsService import LLMsService

import streamlit as st

service = AgentsService()
mcp_servers_service = MCPServersService()
llms_service = LLMsService()

st.header("Δημιουργία AI Agent")

# Initialize a container for the page content.
global container
container = st.container()

with container:
    name = container.text_input("Όνομα")
    system_prompt = container.text_area("System Prompt")

    all_mcp_servers = mcp_servers_service.get_all()
    mcp_server_id = container.selectbox(
        "MCP Server",
        options=[None] + [server['id'] for server in all_mcp_servers],
        format_func=lambda id: "None" if id is None else next(server['name'] for server in all_mcp_servers if server['id'] == id)
    )

    all_llms = llms_service.get_all()
    llm = container.selectbox(
        "LLM",
        options=[None] + [llm for llm in all_llms],
        format_func=lambda name: "None" if name is None else next(llm for llm in all_llms if llm == name)
    )

    if container.button("Save"):
        data = {
            "name": name,
            "system_prompt": system_prompt,
            "mcp_server_id": mcp_server_id,
            "llm": llm
        }

        result = service.add(data)
        
        if isinstance(result, dict) and "error" in result:
            container.error(f"Σφάλμα: {result['error']}")
        else:
            st.switch_page("crud/pages/agent/all_agents.py")