# This page allows the user to view an MCP Server entry by its ID.
from crud.services.RestAPIsService import RestAPIsService
from crud.services.WebsitesService import WebsitesService
from crud.services.MCPServersService import MCPServersService

from fastmcp import FastMCP

import asyncio
import httpx
import streamlit as st

id = st.query_params['id'] if st.query_params['id'] else None
if not id:
    st.error("Λείπει το ID του MCP Server")
    st.stop()

service = MCPServersService()
rest_apis_service = RestAPIsService()
websites_service = WebsitesService()

# Initialize a container for the page content.
global container
container = st.container()

with container:
    entry = service.get_by_id(id)
    if isinstance(entry, dict) and "error" in entry:
        container.error(f"Σφάλμα: {entry['error']}")
        st.stop()

    container.header(entry['name'])

    load_text = container.text("Φορτώνονται τα διαθέσιμα tools...")

    if entry['type'] == 'Rest API':
        # Load REST API information for the MCP server.
        rest_api = rest_apis_service.get_by_id(entry['restapi_id'])

        # Create an HTTP client for your API.
        client = httpx.AsyncClient(base_url=rest_api['domain'])

        # Load your OpenAPI spec.
        openapi_spec = httpx.get(rest_api['domain'] + rest_api['openapi_spec']).json()

        # Create the MCP server
        mcp = FastMCP.from_openapi(
            openapi_spec=openapi_spec,
            client=client,
            name=entry['name']
        )

        # Display the MCP server tools.
        tools = asyncio.run(mcp.list_tools())

        header = container.columns([1, 3.5])
        header[0].markdown("**Όνομα**")
        header[1].markdown("**Περιγραφή**")

        for tool in tools:
            row = container.columns([1, 3.5])
            row[0].markdown(tool.name)
            row[1].markdown(tool.description)

        load_text.empty()