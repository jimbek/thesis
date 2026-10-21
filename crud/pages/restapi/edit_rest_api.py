# This page allows the user to edit an existing REST API.
from crud.services.RestAPIsService import RestAPIsService

import streamlit as st

id = st.query_params['id'] if st.query_params['id'] else None
if not id:
    st.error("Λείπει το ID του REST API")
    st.stop()

service = RestAPIsService()

st.header("Επεξεργασία REST API")

# Initialize a container for the page content.
global container
container = st.container()

with container:
    api = service.get_by_id(id)
    if isinstance(api, dict) and "error" in api:
        container.error(f"Σφάλμα: {api['error']}")
        st.stop()
    
    name = container.text_input("Όνομα", value=api.get('name'))
    description = container.text_area("Περιγραφή", value=api.get('description'))
    domain = container.text_input("Domain", value=api.get('domain'))
    openapi_spec = container.text_input("OpenAPI Spec", value=api.get('openapi_spec'))

    if container.button("Save"):
        data = {
            "name": name,
            "description": description,
            "domain": domain,
            "openapi_spec": openapi_spec,
        }

        result = service.edit(id,data)
        
        if isinstance(result, dict) and "error" in result:
            container.error(f"Σφάλμα: {result['error']}")
        else:
            st.switch_page("crud/pages/restapi/all_rest_apis.py")