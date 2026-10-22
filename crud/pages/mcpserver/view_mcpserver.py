# This page allows the user to view an MCP Server entry by its ID.
from crud.library.FastWebMCP import FastWebMCP
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
        specs = httpx.get(rest_api['domain'] + rest_api['openapi_spec']).json()

        # Create the MCP server
        mcp = FastMCP.from_openapi(
            openapi_spec=specs,
            client=client,
            name=entry['name']
        )

        # Display the MCP server tools.
        tools = asyncio.run(mcp.list_tools())

        header = container.columns([0.2, 1, 3.5])
        header[0].markdown("**#**")
        header[1].markdown("**Όνομα**")
        header[2].markdown("**Περιγραφή**")

        index = 1
        for tool in tools:
            row = container.columns([0.2, 1, 3.5])

            row[0].markdown(str(index))
            row[1].markdown(tool.name)
            row[2].markdown(tool.description)

            index += 1

        load_text.empty()
    elif entry['type'] == 'Website':
        # Load Website information for the MCP server.
        website = websites_service.get_by_id(entry['website_id'])

        # Retrieve the tools from the WebMCP server.
        tools = FastWebMCP.list_tools(website['domain'])

        # Display the website tools.
        header = container.columns([0.2, 1, 3.5])
        header[0].markdown("**#**")
        header[1].markdown("**Όνομα**")
        header[2].markdown("**Περιγραφή**")

        index = 1
        for tool in tools:
            row = container.columns([0.2, 1, 3.5])

            row[0].markdown(str(index))
            row[1].markdown(tool['name'])
            row[2].markdown(tool['description'])

            index += 1

        load_text.empty()