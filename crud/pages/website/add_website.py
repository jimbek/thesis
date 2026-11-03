# Η σελίδα επιτρέπει την προσθήκη νέου Website.
from crud.services.WebsitesService import WebsitesService

import streamlit as st

service = WebsitesService()

st.header("Δημιουργία Website", divider="gray")

global container
container = st.container()

with container:
    name = container.text_input("Όνομα", placeholder="Εισάγετε το όνομα του Website")
    description = container.text_area("Περιγραφή", placeholder="Εισάγετε την περιγραφή του Website")
    domain = container.text_input("Domain", placeholder="https://example.com")

    if container.button("Αποθήκευση"):
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