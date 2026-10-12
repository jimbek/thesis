# This page allows the user to delete a RestAPI entry by its ID.
from crud.repos.RestAPIsRepository import RestAPIsRepository

import streamlit as st

id = st.query_params['id'] if st.query_params['id'] else None
if not id:
    st.error("Λείπει το ID του REST API")
    st.stop()

repo = RestAPIsRepository()

st.header("Διαγραφή REST API")

# Initialize a container for the page content.
global container
container = st.container()

with container:
    entry = repo.get_by_id(id)
    if not entry:
        st.error("Δεν υπάρχει RestAPI με αυτό το ID.")
        st.stop()

    st.html("Είστε σίγουροι ότι θέλετε να διαγράψετε το REST API με domain: <b>" + entry['domain'] + "</b>;")
    
    if container.button("Διαγραφή"):
        result = repo.delete(id)
        if result and 'message' in result:
            st.error(result['message'])
        else:
            st.switch_page("crud/pages/restapi/index.py")