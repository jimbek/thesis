# This page allows the user to add a new REST API.
from crud.repos.RestAPIsRepository import RestAPIsRepository

import streamlit as st

repo = RestAPIsRepository()

st.header("Δημιουργία REST API")

# Initialize a container for the page content.
global container
container = st.container()

with container:
    name = container.text_input("Όνομα")
    description = container.text_area("Περιγραφή")
    domain = container.text_input("Domain")
    openapi_spec = container.text_input("OpenAPI Spec")

    if container.button("Save"):
        data = {
            "name": name,
            "description": description,
            "domain": domain,
            "openapi_spec": openapi_spec,
        }

        result = repo.add(data)
        
        if isinstance(result, dict) and "message" in result:
            container.error(f"Σφάλμα: {result['message']}")
        else:
            st.switch_page("crud/pages/restapi/index.py")