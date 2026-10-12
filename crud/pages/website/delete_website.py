# This page allows the user to delete a Website entry by its ID.
from crud.repos.WebsitesRepository import WebsitesRepository

import streamlit as st

id = st.query_params['id'] if st.query_params['id'] else None
if not id:
    st.error("Λείπει το ID του Website")
    st.stop()

repo = WebsitesRepository()

st.header("Διαγραφή Website")

# Initialize a container for the page content.
global container
container = st.container()

with container:
    entry = repo.get_by_id(id)
    if not entry:
        st.error("Δεν υπάρχει Website με αυτό το ID.")
        st.stop()

    st.html("Είστε σίγουροι ότι θέλετε να διαγράψετε το Website με domain: <b>" + entry['domain'] + "</b>;")
    
    if container.button("Διαγραφή"):
        result = repo.delete(id)
        if result and 'message' in result:
            st.error(result['message'])
        else:
            st.switch_page("crud/pages/website/all_websites.py")