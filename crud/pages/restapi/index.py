# This page displays the list of existing REST APIs.
from crud.services.RestAPIsService import RestAPIsService

import streamlit as st

service = RestAPIsService()

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

    container.header("Rest APIs", divider="gray")
    
    if container.button("New +", type="primary"):
        st.switch_page("crud/pages/restapi/add_rest_api.py")

    header = container.columns([1, 2.5, 1.5, 1.5, 0.5])
    header[0].markdown("**Όνομα**")
    header[1].markdown("**Περιγραφή**")
    header[2].markdown("**Domain**")
    header[3].markdown("**Τεκμηρίωση**")
    header[4].markdown("**Ενέργειες**")

    for api in service.get_all():
        row = container.columns([1, 2.5, 1.5, 1.5, 0.5])

        row[0].markdown(api.get('name'))
        row[1].markdown(api.get('description'))
        row[2].markdown(api.get('domain'))
        row[3].markdown(api.get('openapi_spec'))

        action_buttons = row[4].columns(2)
        action_buttons[0].page_link(
            "crud/pages/restapi/edit_rest_api.py",
            label = "",
            icon = ":material/edit:",
            query_params = {"id": api['id']})

        action_buttons[1].page_link(
            "crud/pages/restapi/delete_rest_api.py",
            label = "",
            icon = ":material/delete:",
            query_params = {"id": api['id']})