# This page displays the list of existing Processes of an AI Agent.
from crud.services.ProcessesService import ProcessesService

import streamlit as st

agent_id = st.query_params['agent_id'] if st.query_params['agent_id'] else None
if not agent_id:
    st.error("Λείπει το ID του AI Agent")
    st.stop()

service = ProcessesService()

# Initialize a container for the page content.
global container
container = st.container()

with container:
    processes = service.get_by_agent_id(agent_id)
    if isinstance(processes, dict) and "error" in processes:
        container.error(f"Σφάλμα: {processes['error']}")
        st.stop()
    
    container.markdown(
        """
            <style>
                .st-emotion-cache-r6kf2v {
                    max-width: 90%;
                }

                .st-emotion-cache-uvlrfw {
                    width: 0;
                    max-width: 0;
                }
            </style>
        """,
        unsafe_allow_html=True,
    )

    container.header("Processes", divider="gray")
    
    if container.button("New +", type="primary"):
        st.switch_page("crud/pages/process/add_process.py", query_params={"agent_id": agent_id})

    header = container.columns([4, 0.5])
    header[0].markdown("**Port**")
    header[1].markdown("**Ενέργειες**")

    for process in processes:
        row = container.columns([4, 0.5])

        row[0].markdown(process.get('port'))

        action_buttons = row[1].columns(1)
        action_buttons[0].page_link(
            "crud/pages/process/delete_process.py",
            label = "",
            icon = ":material/delete:",
            query_params = {"id": process['id']}
        )