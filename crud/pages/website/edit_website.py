# This page allows the user to edit an existing Website.
from crud.services.WebsitesService import WebsitesService

import streamlit as st

id = st.query_params['id'] if st.query_params['id'] else None
if not id:
    st.error("Λείπει το ID του Website")
    st.stop()

service = WebsitesService()

st.header("Επεξεργασία Website")

# Initialize a container for the page content.
global container
container = st.container()

with container:
    website = service.get_by_id(id)
    if isinstance(website, dict) and "error" in website:
        container.error(f"Σφάλμα: {website['error']}")
        st.stop()
    
    name = container.text_input("Όνομα", value=website.get('name'))
    description = container.text_area("Περιγραφή", value=website.get('description'))
    domain = container.text_input("Domain", value=website.get('domain'))

    if container.button("Save"):
        data = {
            "name": name,
            "description": description,
            "domain": domain
        }

        result = service.edit(id, data)
        st.toast(result)
        
        if isinstance(result, dict) and "error" in result:
            container.error(f"Σφάλμα: {result['error']}")
        else:
            st.switch_page("crud/pages/website/all_websites.py")