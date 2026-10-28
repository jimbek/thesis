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
    
    port = container.text_input("Port")

    if container.button("Save"):
        data = {
            "agent_id": agent_id,
            "port": port
        }

        result = service.add(data)
        
        if result:
            st.switch_page("crud/pages/process/all_processes.py", query_params={"agent_id": agent_id})
        else:
            container.error("Σφάλμα κατά την προσθήκη του Process.")