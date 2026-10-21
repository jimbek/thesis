# This page allows the user to edit an existing MCP Server.
from crud.services.MCPServersService import MCPServersService
from crud.services.RestAPIsService import RestAPIsService
from crud.services.WebsitesService import WebsitesService

import streamlit as st

id = st.query_params['id'] if st.query_params['id'] else None
if not id:
    st.error("Λείπει το ID του MCP Server")
    st.stop()

service = MCPServersService()
rest_apis_service = RestAPIsService()
websites_service = WebsitesService()

st.header("Επεξεργασία MCP Server")

# Initialize a container for the page content.
global container
container = st.container()

with container:
    mcpserver = service.get_by_id(id)
    if isinstance(mcpserver, dict) and "error" in mcpserver:
        container.error(f"Σφάλμα: {mcpserver['error']}")
        st.stop()
    
    name = container.text_input("Όνομα", value=mcpserver.get('name') if mcpserver else "")
    instructions = container.text_area("Οδηγίες", value=mcpserver.get('instructions') if mcpserver else "")

    all_rest_apis = rest_apis_service.get_all()
    rest_api_id = container.selectbox(
        "REST API",
        options=[None] + [api['id'] for api in all_rest_apis],
        format_func=lambda id: "None" if id is None else next(api['name'] for api in all_rest_apis if api['id'] == id),
        index = 0 if mcpserver.get('type') == "Website" else ([None] + [api['id'] for api in all_rest_apis]).index(mcpserver.get('restapi_id'))
    )

    all_websites = websites_service.get_all()
    website_id = container.selectbox(
        "Website",
        options=[None] + [website['id'] for website in all_websites],
        format_func=lambda id: "None" if id is None else next(website['name'] for website in all_websites if website['id'] == id),
        index = 0 if mcpserver.get('type') == "Rest API" else ([None] + [website['id'] for website in all_websites]).index(mcpserver.get('website_id'))
    )

    if container.button("Save"):
        data = {
            "name": name,
            "instructions": instructions,
            "restapi_id": rest_api_id,
            "website_id": website_id
        }

        result = service.edit(id, data)
        
        if isinstance(result, dict) and "error" in result:
            container.error(f"Σφάλμα: {result['error']}")
        else:
            st.switch_page("crud/pages/mcpserver/index.py")