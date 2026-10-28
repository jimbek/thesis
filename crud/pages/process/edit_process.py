# This page allows the user to edit an existing Process.
from crud.services.ProcessesService import ProcessesService
from crud.services.AgentsService import AgentsService

import streamlit as st

id = st.query_params['id'] if st.query_params['id'] else None
if not id:
    st.error("Λείπει το ID του Process")
    st.stop()

service = ProcessesService()
agent_service = AgentsService()

st.header("Επεξεργασία Process")

# Initialize a container for the page content.
global container
container = st.container()

with container:
    process = service.get_by_id(id)
    if isinstance(process, dict) and "error" in process:
        container.error(f"Σφάλμα: {process['error']}")
        st.stop()

    port = container.text_input("Port", value=process.get('port', '8000'))

    if container.button("Save"):
        data = {
            "id": id,
            "agent_id": process.get('agent_id'),
            "port": port
        }

        result = service.edit(id, data)
        
        if result:
            st.switch_page("crud/pages/process/all_processes.py", query_params={"agent_id": process.get('agent_id')})
        else:
            container.error("Σφάλμα κατά την επεξεργασία του Process.")