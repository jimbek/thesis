# This page allows the user to add a new LLM.
from crud.services.LLMsService import LLMsService

import streamlit as st

service = LLMsService()

st.header("Εγκατάσταση LLM")

# Initialize a container for the page content.
global container
container = st.container()

with container:
    name = container.text_input("Όνομα")

    if container.button("Save"):
        st.toast("Η εγκατάσταση του μοντέλου ξεκίνησε, παρακαλώ περιμένετε...", icon=":material/download:")
        result = service.download_model(name)
        
        if result:
            st.switch_page("crud/pages/llm/all_llms.py")
        else:
            container.error("Σφάλμα κατά τη λήψη του μοντέλου.")