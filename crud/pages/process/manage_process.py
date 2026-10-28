# This page allows the user to manage the Process of an AI Agent entry by its ID.
from crud.services.AgentsService import AgentsService
from crud.services.MCPServersService import MCPServersService
from crud.services.ProcessesService import ProcessesService

import streamlit as st

id = st.query_params['id'] if st.query_params['id'] else None
if not id:
    st.error("Λείπει το ID του Process")
    st.stop()

service = ProcessesService()

st.header("Διαχείριση Process")

# Initialize a container for the page content.
global container
container = st.container()

with container:
    process = service.get_by_id(id)

    if not process:
        container.error("Δεν βρέθηκε το process.")
        st.stop()
    
    if isinstance(process, dict) and "error" in process:
        container.error(f"Σφάλμα: {process['error']}")
        st.stop()

    def run_process():
        container.toast(f"Εκκίνηση του process...")
        st.rerun()

    def delete_process():
        container.toast(f"Διαγραφή του process...")
        st.rerun()

    # Create side-by-side buttons using columns
    col1, col2 = st.columns([1.5, 1.5])

    if process['pid'] and service.is_running(process['pid']):
        if col1.button("Διακοπή", icon=":material/stop:", use_container_width=True):
            delete_process()
    else:
        if col1.button("Εκτέλεση", icon=":material/play_arrow:", use_container_width=True):
            run_process()