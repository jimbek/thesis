# This page allows the user to delete an AI Agent entry by its ID.
from crud.services.AgentsService import AgentsService

import streamlit as st

id = st.query_params['id'] if st.query_params['id'] else None
if not id:
    st.error("Λείπει το ID του AI Agent")
    st.stop()

service = AgentsService()

st.header("Διαγραφή AI Agent")

# Initialize a container for the page content.
global container
container = st.container()

with container:
    entry = service.get_by_agent_id(id)
    if isinstance(entry, dict) and "error" in entry:
        container.error(f"Σφάλμα: {entry['error']}")
        st.stop()

    container.html("Είστε σίγουροι ότι θέλετε να διαγράψετε το AI Agent με όνομα: <b>" + entry['name'] + "</b>;")
    
    if container.button("Διαγραφή"):
        result = service.delete(id)
        if result and 'error' in result:
            container.error(result['error'])
        else:
            st.switch_page("crud/pages/agent/all_agents.py")