# Η σελίδα επιτρέπει την επεξεργασία ενός υπάρχοντος AI Agent.
from crud.services.AgentsService import AgentsService
from crud.services.MCPServersService import MCPServersService

import streamlit as st

id = st.query_params['id'] if st.query_params['id'] else None
if not id:
    st.error("Λείπει το ID του AI Agent")
    st.stop()

service = AgentsService()
mcp_servers_service = MCPServersService()

st.header("Επεξεργασία AI Agent")

global container
container = st.container()

with container:
    agent = service.get_by_agent_id(id)
    if isinstance(agent, dict) and "error" in agent:
        container.error(f"Σφάλμα: {agent['error']}")
        st.stop()
    
    name = container.text_input("Όνομα", value=agent.get('name') if agent else "")
    system_prompt = container.text_area("System Prompt", value=agent.get('system_prompt') if agent else "")

    all_mcp_servers = mcp_servers_service.get_all()
    mcp_server_ids = container.multiselect(
        "MCP Servers",
        options=[server['id'] for server in all_mcp_servers],
        format_func=lambda id: "None" if id is None else next(server['name'] for server in all_mcp_servers if server['id'] == id),
        default=agent.get('mcp_server_ids')
    )

    if container.button("Save"):
        data = {
            "name": name,
            "system_prompt": system_prompt,
            "mcp_server_ids": mcp_server_ids
        }

        result = service.edit(id, data)
        
        if isinstance(result, dict) and "error" in result:
            container.error(f"Σφάλμα: {result['error']}")
        else:
            st.switch_page("crud/pages/agent/all_agents.py")