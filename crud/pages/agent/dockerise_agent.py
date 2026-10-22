# This page allows the user to dockerise an AI Agent entry by its ID.
from crud.services.AgentsService import AgentsService
from crud.services.DockerService import DockerService

import streamlit as st

id = st.query_params['id'] if st.query_params['id'] else None
if not id:
    st.error("Λείπει το ID του AI Agent")
    st.stop()

service = AgentsService()
docker_service = DockerService()

st.header("Docker - AI Agent")

# Initialize a container for the page content.
global container
container = st.container()

with container:
    entry = service.get_by_id(id)
    if isinstance(entry, dict) and "error" in entry:
        container.error(f"Σφάλμα: {entry['error']}")
        st.stop()

    container.markdown(f"Αυτόματη δημιουργία / διαγραφή Docker container για τον <b>{entry['name']}</b> AI Agent.", unsafe_allow_html=True);

    def run_agent(agent):
        container.toast(f"Starting {agent['name']}...")
        # docker_service.run_container(image=agent['image'], name=agent['name'])
        container.toast(f"Started running {agent['name']}.")

    def pause_agent(agent):
        container.toast(f"Pausing {agent['name']}...")
        # docker_service.pause_container(name=agent['name'])
        container.toast(f"Paused {agent['name']}.")