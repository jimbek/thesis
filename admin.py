# Defines pages and navigation for the admin interface.
# Pages are defined in the pages/ directory and imported here.
from crud.repos.RestAPIsRepository import RestAPIsRepository
from crud.repos.WebsitesRepository import WebsitesRepository
from crud.repos.MCPServersRepository import MCPServersRepository
from crud.repos.LLMsRepository import LLMsRepository
from crud.repos.AgentsRepository import AgentsRepository

import streamlit as st

restapis_repo = RestAPIsRepository()
websites_repo = WebsitesRepository()
mcpservers_repo = MCPServersRepository()
llms_repo = LLMsRepository()
agents_repo = AgentsRepository()

# Seed the db
if restapis_repo.table_exists('RestAPIs') is False:
    restapis_repo.apply_migrations()

if websites_repo.table_exists('Websites') is False:
    websites_repo.apply_migrations()

if mcpservers_repo.table_exists('MCPServers') is False:
    mcpservers_repo.apply_migrations()

if llms_repo.table_exists('LLMs') is False:
    llms_repo.apply_migrations()

if agents_repo.table_exists('Agents') is False:
    agents_repo.apply_migrations()

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