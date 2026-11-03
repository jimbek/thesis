# Η σελίδα εμφανίζει τους διαθέσιμους MCP Servers.
from crud.services.MCPServersService import MCPServersService

import streamlit as st

service = MCPServersService()

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

    container.header("MCP Servers", divider="gray")

    if container.button("Νέος +", type="primary"):
        st.switch_page("crud/pages/mcpserver/add_mcpserver.py")

    header = container.columns([2, 1, 1.5, 0.5])
    header[0].markdown("**Όνομα**")
    header[1].markdown("**Τύπος**")
    header[2].markdown("**Πηγή**")
    header[3].markdown("**Ενέργειες**")

    for mcpserver in service.get_all():
        row = container.columns([2, 1, 1.5, 0.5])

        row[0].markdown(mcpserver.get('name'))
        row[1].markdown(mcpserver.get('type'))
        row[2].markdown(mcpserver.get('source'))

        action_buttons = row[3].columns(2)
        action_buttons[0].page_link(
            "crud/pages/mcpserver/edit_mcpserver.py",
            label = "",
            icon = ":material/edit:",
            query_params = {"id": mcpserver['id']})

        action_buttons[1].page_link(
            "crud/pages/mcpserver/delete_mcpserver.py",
            label = "",
            icon = ":material/delete:",
            query_params = {"id": mcpserver['id']})