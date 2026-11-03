# Η σελίδα επιτρέπει την προσθήκη νέου REST API.
from crud.services.RestAPIsService import RestAPIsService

import streamlit as st

service = RestAPIsService()

st.header("Δημιουργία REST API", divider="gray")

global container
container = st.container()

with container:
    name = container.text_input("Όνομα", placeholder="Εισάγετε το όνομα του REST API")
    description = container.text_area("Περιγραφή", placeholder="Εισάγετε την περιγραφή του REST API")
    domain = container.text_input("Domain", placeholder="https://example.com")
    openapi_spec = container.text_input("OpenAPI Spec", placeholder="/openapi.json")

    container.info("Το Open API version πρέπει αν είναι >= 3.0.")

    if container.button("Αποθήκευση"):
        data = {
            "name": name,
            "description": description,
            "domain": domain,
            "openapi_spec": openapi_spec,
        }

        result = service.add(data)
        
        if isinstance(result, dict) and "error" in result:
            container.error(f"Σφάλμα: {result['error']}")
        else:
            st.switch_page("crud/pages/restapi/all_rest_apis.py")