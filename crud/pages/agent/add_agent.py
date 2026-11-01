# This page allows the user to add a new AI Agent.
from crud.services.AgentsService import AgentsService
from crud.services.MCPServersService import MCPServersService

import streamlit as st

service = AgentsService()
mcp_servers_service = MCPServersService()

st.header("Δημιουργία AI Agent")

# Initialize a container for the page content.
global container
container = st.container()

with container:
    name = container.text_input("Όνομα")
    system_prompt = container.text_area("System Prompt")

    all_mcp_servers = mcp_servers_service.get_all()
    mcp_server_ids = container.multiselect(
        "MCP Servers",
        options=[server['id'] for server in all_mcp_servers],
        format_func=lambda id: "None" if id is None else next(server['name'] for server in all_mcp_servers if server['id'] == id)
    )

    if container.button("Save"):
        data = {
            "name": name,
            "system_prompt": system_prompt,
            "mcp_server_ids": mcp_server_ids
        }

        result = service.add(data)
        
        if isinstance(result, dict) and "error" in result:
            container.error(f"Σφάλμα: {result['error']}")
        else:
            st.switch_page("crud/pages/agent/all_agents.py")