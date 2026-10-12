# This page allows the user to edit an existing Website.
from crud.repos.WebsitesRepository import WebsitesRepository

import streamlit as st

id = st.query_params['id'] if st.query_params['id'] else None
if not id:
    st.error("Λείπει το ID του Website")
    st.stop()

repo = WebsitesRepository()

st.header("Επεξεργασία Website")

# Initialize a container for the page content.
global container
container = st.container()

with container:
    website = repo.get_by_id(id)
    if not website:
        container.error("Δεν βρέθηκε το Website")
        st.stop()
    
    name = container.text_input("Όνομα", value=website.get('name'))
    description = container.text_area("Περιγραφή", value=website.get('description'))
    domain = container.text_input("Domain", value=website.get('domain'))

    if container.button("Save"):
        data = {
            "id": id,
            "name": name,
            "description": description,
            "domain": domain
        }

        result = repo.edit(data)
        
        if isinstance(result, dict) and "message" in result:
            container.error(f"Σφάλμα: {result['message']}")
        else:
            st.switch_page("crud/pages/website/all_websites.py")