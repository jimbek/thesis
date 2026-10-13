# This page allows the user to delete an MCP Server entry by its ID.
from crud.repos.MCPServersRepository import MCPServersRepository

import streamlit as st

id = st.query_params['id'] if st.query_params['id'] else None
if not id:
    st.error("Λείπει το ID του MCP Server")
    st.stop()

repo = MCPServersRepository()

st.header("Διαγραφή MCP Server")

# Initialize a container for the page content.
global container
container = st.container()

with container:
    entry = repo.get_by_id(id)
    if not entry:
        st.error("Δεν υπάρχει MCP Server με αυτό το ID.")
        st.stop()

    st.html("Είστε σίγουροι ότι θέλετε να διαγράψετε τον MCP Server με όνομα: <b>" + entry['name'] + "</b>;")
    
    if container.button("Διαγραφή"):
        result = repo.delete(id)
        if result and 'message' in result:
            st.error(result['message'])
        else:
            st.switch_page("crud/pages/mcpserver/all_mcpservers.py")