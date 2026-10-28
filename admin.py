# Defines pages and navigation for the admin interface.
# Pages are defined in the pages/ directory and imported here.
import streamlit as st

pages = [
    st.Page("crud/pages/restapi/all_rest_apis.py", title="REST APIs"),
    st.Page("crud/pages/restapi/add_rest_api.py", title="Νέο REST API", visibility = "hidden"),
    st.Page("crud/pages/restapi/edit_rest_api.py", title="Επεξεργασία REST API", visibility = "hidden"),
    st.Page("crud/pages/restapi/delete_rest_api.py", title="Διαγραφή REST API", visibility = "hidden"),
    st.Page("crud/pages/website/all_websites.py", title="Websites"),
    st.Page("crud/pages/website/add_website.py", title="Νέο Website", visibility = "hidden"),
    st.Page("crud/pages/website/edit_website.py", title="Επεξεργασία Website", visibility = "hidden"),
    st.Page("crud/pages/website/delete_website.py", title="Διαγραφή Website", visibility = "hidden"),
    st.Page("crud/pages/mcpserver/index.py", title="MCP Servers", default = True),
    st.Page("crud/pages/mcpserver/add_mcpserver.py", title="Νέος MCP Server", visibility = "hidden"),
    st.Page("crud/pages/mcpserver/edit_mcpserver.py", title="Επεξεργασία MCP Server", visibility = "hidden"),
    st.Page("crud/pages/mcpserver/delete_mcpserver.py", title="Διαγραφή MCP Server", visibility = "hidden"),
    st.Page("crud/pages/mcpserver/view_mcpserver.py", title="Προβολή MCP Server", visibility = "hidden"),
    st.Page("crud/pages/llm/all_llms.py", title="LLMs"),
    st.Page("crud/pages/llm/add_llm.py", title="Νέο LLM", visibility = "hidden"),
    st.Page("crud/pages/llm/delete_llm.py", title="Διαγραφή LLM", visibility = "hidden"),
    st.Page("crud/pages/agent/all_agents.py", title="AI Agents"),
    st.Page("crud/pages/agent/add_agent.py", title="Νέος Agent", visibility = "hidden"),
    st.Page("crud/pages/agent/edit_agent.py", title="Επεξεργασία Agent", visibility = "hidden"),
    st.Page("crud/pages/agent/delete_agent.py", title="Διαγραφή Agent", visibility = "hidden"),
    st.Page("crud/pages/process/all_processes.py", title="Processes", visibility = "hidden"),
    st.Page("crud/pages/process/add_process.py", title="Νέο Process", visibility = "hidden"),
    st.Page("crud/pages/process/edit_process.py", title="Επεξεργασία Process", visibility = "hidden"),
    st.Page("crud/pages/process/delete_process.py", title="Διαγραφή Process", visibility = "hidden"),
    st.Page("crud/pages/process/manage_process.py", title="Διαχείριση Process", visibility = "hidden")
]

pg = st.navigation(pages)
pg.run()