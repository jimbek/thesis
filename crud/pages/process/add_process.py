# This page allows the user to add a new Process.
from crud.services.ProcessesService import ProcessesService
from crud.services.AgentsService import AgentsService

import streamlit as st

agent_id = st.query_params['agent_id'] if st.query_params['agent_id'] else None
if not agent_id:
    st.error("Λείπει το ID του AI Agent")
    st.stop()

service = ProcessesService()
agent_service = AgentsService()

st.header("Προσθήκη Process")

# Initialize a container for the page content.
global container
container = st.container()

with container:
    agent = agent_service.get_by_agent_id(agent_id)
    if isinstance(agent, dict) and "error" in agent:
        container.error(f"Σφάλμα: {agent['error']}")
        st.stop()
    
    port = container.number_input("Port", min_value=8000, max_value=8010, value=8001)

    if container.button("Save"):
        payload = {
            "port": port,
            "system_prompt": agent.get('system_prompt'),
            "llm": agent.get('llm'),
            "mcp_server_ids": agent.get('mcp_server_ids')
        }
        
        result = service.run_process(payload)
        if isinstance(result, dict) and "error" in result:
            container.error(f"Σφάλμα: {result['error']}")
            st.stop()

        data = {
            "pid": result.get('pid'),
            "agent_id": agent_id,
            "port": port
        }

        result = service.add(data)
        if isinstance(result, dict) and "error" in result:
            container.error(f"Σφάλμα: {result['error']}")
            st.stop()
        else:
            st.switch_page("crud/pages/process/all_processes.py", query_params={"agent_id": agent_id})