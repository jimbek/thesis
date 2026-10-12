# This page displays the list of existing Websites.
from crud.repos.WebsitesRepository import WebsitesRepository

import streamlit as st

repo = WebsitesRepository()

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

    container.header("Websites", divider="gray")

    if container.button("New +", type="primary"):
        st.switch_page("crud/pages/website/add_website.py")

    header = container.columns([1, 3.5, 1.5, 0.5])
    header[0].markdown("**Όνομα**")
    header[1].markdown("**Περιγραφή**")
    header[2].markdown("**Domain**")
    header[3].markdown("**Ενέργειες**")

    for website in repo.get_all():
        row = container.columns([1, 3.5, 1.5, 0.5])

        row[0].markdown(website.get('name'))
        row[1].markdown(website.get('description'))
        row[2].markdown(website.get('domain'))

        action_buttons = row[3].columns(2)
        action_buttons[0].page_link(
            "crud/pages/website/edit_website.py",
            label = "",
            icon = ":material/edit:",
            query_params = {"id": website['id']})

        action_buttons[1].page_link(
            "crud/pages/website/delete_website.py",
            label = "",
            icon = ":material/delete:",
            query_params = {"id": website['id']})