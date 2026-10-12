# Defines pages and navigation for the admin interface.
# Pages are defined in the pages/ directory and imported here.
import streamlit as st

pages = [
    st.Page("crud/pages/restapi/index.py", title="REST APIs"),
    st.Page("crud/pages/restapi/add_rest_api.py", title="Νέο REST API", visibility = "hidden"),
    st.Page("crud/pages/restapi/edit_rest_api.py", title="Επεξεργασία REST API", visibility = "hidden"),
    st.Page("crud/pages/restapi/delete_rest_api.py", title="Διαγραφή REST API", visibility = "hidden"),
    st.Page("crud/pages/website/all_websites.py", title="Websites"),
    st.Page("crud/pages/mcpserver/all_mcpservers.py", title="MCP Servers")
]

pg = st.navigation(pages)
pg.run()