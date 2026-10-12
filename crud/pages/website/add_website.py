# This page allows the user to add a new Website.
from crud.repos.WebsitesRepository import WebsitesRepository

import streamlit as st

repo = WebsitesRepository()

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

        result = repo.add(data)
        
        if isinstance(result, dict) and "message" in result:
            container.error(f"Σφάλμα: {result['message']}")
        else:
            st.switch_page("crud/pages/website/all_websites.py")