# This page allows the user to add a new MCP Server.
from crud.services.MCPServersService import MCPServersService
from crud.services.RestAPIsService import RestAPIsService
from crud.services.WebsitesService import WebsitesService

import streamlit as st

service = MCPServersService()
rest_apis_service = RestAPIsService()
websites_service = WebsitesService()

st.header("Δημιουργία MCP Server")

# Initialize a container for the page content.
global container
container = st.container()

with container:
    name = container.text_input("Όνομα")
    instructions = container.text_area("Οδηγίες")

    all_rest_apis = rest_apis_service.get_all()
    rest_api_id = container.selectbox(
        "REST API",
        options=[None] + [api['id'] for api in all_rest_apis],
        format_func=lambda id: "None" if id is None else next(api['name'] for api in all_rest_apis if api['id'] == id)
    )

    all_websites = websites_service.get_all()
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

        result = service.add(data)
        
        if isinstance(result, dict) and "error" in result:
            container.error(f"Σφάλμα: {result['error']}")
        else:
            st.switch_page("crud/pages/mcpserver/index.py")