# This page displays the list of existing AI Agents.
from crud.services.AgentsService import AgentsService

import streamlit as st

service = AgentsService()

# Initialize a container for the page content.
global container
container = st.container()

with container:
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

    container.header("AI Agents", divider="gray")

    if container.button("New +", type="primary"):
        st.switch_page("crud/pages/agent/add_agent.py")

    header = container.columns([1.5, 3.5, 1, 1.5, 0.5])
    header[0].markdown("**Όνομα**")
    header[1].markdown("**Οδηγίες**")
    header[2].markdown("**LLM**")
    header[3].markdown("**# MCP Servers**")
    header[4].markdown("**Ενέργειες**")

    for agent in service.get_all():
        row = container.columns([1.5, 3.5, 1, 1.5, 0.5])

        row[0].markdown(agent.get('name'))
        row[1].markdown(agent.get('system_prompt'))
        row[2].markdown(agent.get('llm'))
        row[3].markdown(len(agent.get('mcp_server_ids')))

        action_buttons = row[4].columns(3)
        action_buttons[0].page_link(
            "crud/pages/agent/manage_agent.py",
            label = "",
            icon = ":material/terminal:",
            query_params = {"id": agent['id']}
        )
        action_buttons[1].page_link(
            "crud/pages/agent/edit_agent.py",
            label = "",
            icon = ":material/edit:",
            query_params = {"id": agent['id']}
        )
        action_buttons[2].page_link(
            "crud/pages/agent/delete_agent.py",
            label = "",
            icon = ":material/delete:",
            query_params = {"id": agent['id']}
        )