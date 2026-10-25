# This page allows the user to chat with an AI Agent entry by its ID.
from crud.services.AgentsService import AgentsService

import streamlit as st

id = st.query_params['id'] if st.query_params['id'] else None
if not id:
    st.error("Λείπει το ID του AI Agent")
    st.stop()

service = AgentsService()

st.header("Διαχείριση AI Agent")

# Initialize a container for the page content.
global container
container = st.container()

with container:
    entry = service.get_by_id(id)
    if isinstance(entry, dict) and "error" in entry:
        container.error(f"Σφάλμα: {entry['error']}")
        st.stop()

    def run_agent(agent):
        container.toast(f"Starting {agent['name']}...")
        container.toast(f"Started running {agent['name']}.")

    def pause_agent(agent):
        container.toast(f"Pausing {agent['name']}...")
        container.toast(f"Paused {agent['name']}.")

    def delete_agent(agent):
        container.toast(f"Deleting {agent['name']}...")
        container.toast(f"Deleted {agent['name']}.")

    # Create side-by-side buttons using columns
    col1, col2, col3 = st.columns([1.5, 1.5, 1.5])
    
    if col1.button("🚀 Εκτέλεση", use_container_width=True):
        run_agent(entry)

    if col2.button("⏸️ Παύση", use_container_width=True):
        pause_agent(entry)

    if col3.button("🗑️ Διαγραφή", use_container_width=True):
        delete_agent(entry)