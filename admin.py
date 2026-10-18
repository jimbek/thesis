# Defines pages and navigation for the admin interface.
# Pages are defined in the pages/ directory and imported here.
import streamlit as st

pages = [
    st.Page("crud/pages/restapi/index.py", title="REST APIs"),
    st.Page("crud/pages/restapi/add_rest_api.py", title="Νέο REST API", visibility = "hidden"),
    st.Page("crud/pages/restapi/edit_rest_api.py", title="Επεξεργασία REST API", visibility = "hidden"),
    st.Page("crud/pages/restapi/delete_rest_api.py", title="Διαγραφή REST API", visibility = "hidden"),
    st.Page("crud/pages/website/all_websites.py", title="Websites"),
    st.Page("crud/pages/website/add_website.py", title="Νέο Website", visibility = "hidden"),
    st.Page("crud/pages/website/edit_website.py", title="Επεξεργασία Website", visibility = "hidden"),
    st.Page("crud/pages/website/delete_website.py", title="Διαγραφή Website", visibility = "hidden"),
    st.Page("crud/pages/mcpserver/all_mcpservers.py", title="MCP Servers"),
    st.Page("crud/pages/mcpserver/add_mcpserver.py", title="Νέος MCP Server", visibility = "hidden"),
    st.Page("crud/pages/mcpserver/edit_mcpserver.py", title="Επεξεργασία MCP Server", visibility = "hidden"),
    st.Page("crud/pages/mcpserver/delete_mcpserver.py", title="Διαγραφή MCP Server", visibility = "hidden"),
    st.Page("crud/pages/llm/all_llms.py", title="LLMs"),
    st.Page("crud/pages/llm/add_llm.py", title="Νέο LLM", visibility = "hidden"),
    st.Page("crud/pages/llm/delete_llm.py", title="Διαγραφή LLM", visibility = "hidden")
]

pg = st.navigation(pages)
pg.run()