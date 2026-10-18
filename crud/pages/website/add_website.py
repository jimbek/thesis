# This page allows the user to add a new Website.
from crud.services.WebsitesService import WebsitesService

import streamlit as st

service = WebsitesService()

st.header("Δημιουργία Website")

# Initialize a container for the page content.
global container
container = st.container()

with container:
    name = container.text_input("Όνομα")
    description = container.text_area("Περιγραφή")
    domain = container.text_input("Domain")

    if container.button("Save"):
        data = {
            "name": name,
            "description": description,
            "domain": domain
        }

        result = service.add(data)
        
        if isinstance(result, dict) and "error" in result:
            container.error(f"Σφάλμα: {result['error']}")
        else:
            st.switch_page("crud/pages/website/all_websites.py")