# This page allows the user to edit an existing REST API.
from crud.repos.RestAPIsRepository import RestAPIsRepository

import streamlit as st

id = st.query_params['id'] if st.query_params['id'] else None
if not id:
    st.error("Λείπει το ID του REST API")
    st.stop()

repo = RestAPIsRepository()

st.header("Επεξεργασία REST API")

# Initialize a container for the page content.
global container
container = st.container()

with container:
    api = repo.get_by_id(id)
    if not api:
        container.error("Δεν βρέθηκε το REST API")
        st.stop()
    
    name = container.text_input("Όνομα", value=api.get('name'))
    description = container.text_area("Περιγραφή", value=api.get('description'))
    domain = container.text_input("Domain", value=api.get('domain'))
    openapi_spec = container.text_input("OpenAPI Spec", value=api.get('openapi_spec'))

    if container.button("Save"):
        data = {
            "id": id,
            "name": name,
            "description": description,
            "domain": domain,
            "openapi_spec": openapi_spec,
        }

        result = repo.edit(data)
        
        if isinstance(result, dict) and "message" in result:
            container.error(f"Σφάλμα: {result['message']}")
        else:
            st.switch_page("crud/pages/restapi/index.py")