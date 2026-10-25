# This page allows the user to manage the Process of an AI Agent entry by its ID.
from crud.services.AgentsService import AgentsService
from crud.services.ProcessesService import ProcessesService

import streamlit as st

id = st.query_params['id'] if st.query_params['id'] else None
if not id:
    st.error("Λείπει το ID του AI Agent")
    st.stop()

service = ProcessesService()
agents_service = AgentsService()

st.header("Διαχείριση Process")

# Initialize a container for the page content.
global container
container = st.container()

with container:
    entry = agents_service.get_by_agent_id(id)
    if isinstance(entry, dict) and "error" in entry:
        container.error(f"Σφάλμα: {entry['error']}")
        st.stop()

    port = container.number_input("Port", 8000)

    process = service.get_by_agent_id(id)
    if not process:
        st.toast("Το process δεν τρέχει αυτή τη στιγμή.")
    else:
        st.toast(f"Το process {process['name']} τρέχει.")

    def run_process(process: dict):
        container.toast(f"Starting {process['name']}...")
        
        result = service.run_process(process['id'])
        if result == "OK":
            container.toast(f"Started running {process['name']}.")
        else:
            container.toast(f"Failed to start {process['name']}: {result}")

    def pause_process(process: dict):
        container.toast(f"Pausing {process['name']}...")
        result = service.pause_process(process['id'])
        if result == "OK":
            container.toast(f"Paused {process['name']}.")
        else:
            container.toast(f"Failed to pause {process['name']}: {result}")

    def delete_process(process: dict):
        container.toast(f"Deleting {process['name']}...")

        result = service.delete_process(process['id'])
        if result == "OK":
            container.toast(f"Deleted {process['name']}.")
        else:
            container.toast(f"Failed to delete {process['name']}: {result}")

    # Create side-by-side buttons using columns
    col1, col2, col3 = st.columns([1.5, 1.5, 1.5])
    
    if col1.button("🚀 Εκτέλεση", use_container_width=True):
        run_process(entry)

    if col2.button("⏸️ Παύση", use_container_width=True):
        pause_process(entry)

    if col3.button("🗑️ Διαγραφή", use_container_width=True):
        delete_process(entry)