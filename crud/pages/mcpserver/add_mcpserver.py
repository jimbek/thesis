# This page allows the user to add a new MCP Server.
from crud.repos.MCPServersRepository import MCPServersRepository
from crud.repos.RestAPIsRepository import RestAPIsRepository
from crud.repos.WebsitesRepository import WebsitesRepository

import streamlit as st

repo = MCPServersRepository()
rest_apis_repo = RestAPIsRepository()
websites_repo = WebsitesRepository()

st.header("Δημιουργία MCP Server")

# Initialize a container for the page content.
global container
container = st.container()

with container:
    name = container.text_input("Όνομα")
    instructions = container.text_area("Οδηγίες")

    all_rest_apis = rest_apis_repo.get_all()
    rest_api_id = container.selectbox(
        "REST API",
        options=[None] + [api['id'] for api in all_rest_apis],
        format_func=lambda id: "None" if id is None else next(api['name'] for api in all_rest_apis if api['id'] == id)
    )

    all_websites = websites_repo.get_all()
    website_id = container.selectbox(
        "Website",
        options=[None] + [website['id'] for website in all_websites],
        format_func=lambda id: "None" if id is None else next(website['name'] for website in all_websites if website['id'] == id)
    )

    if container.button("Save"):
        data = {
            "name": name,
            "instructions": instructions,
            "restapi_id": rest_api_id,
            "website_id": website_id
        }

        result = repo.add(data)
        
        if isinstance(result, dict) and "message" in result:
            container.error(f"Σφάλμα: {result['message']}")
        else:
            st.switch_page("crud/pages/mcpserver/all_mcpservers.py")