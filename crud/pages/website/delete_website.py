# This page allows the user to delete a Website entry by its ID.
from crud.services.WebsitesService import WebsitesService

import streamlit as st

id = st.query_params['id'] if st.query_params['id'] else None
if not id:
    st.error("Λείπει το ID του Website")
    st.stop()

service = WebsitesService()

st.header("Διαγραφή Website")

# Initialize a container for the page content.
global container
container = st.container()

with container:
    entry = service.get_by_id(id)
    if isinstance(entry, dict) and "error" in entry:
        container.error(f"Σφάλμα: {entry['error']}")
        st.stop()

    container.html("Είστε σίγουροι ότι θέλετε να διαγράψετε το Website με domain: <b>" + entry['domain'] + "</b>;")
    
    if container.button("Διαγραφή"):
        result = service.delete(id)
        if result and 'error' in result:
            container.error(result['error'])
        else:
            st.switch_page("crud/pages/website/all_websites.py")