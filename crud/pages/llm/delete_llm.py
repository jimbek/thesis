# This page allows the user to delete an LLM.
from crud.services.Ollama import OllamaService

import streamlit as st

name = st.query_params['name'] if st.query_params['name'] else None
if not name:
    st.error("Λείπει το όνομα του LLM")
    st.stop()

service = OllamaService()

st.header("Διαγραφή LLM")

# Initialize a container for the page content.
global container
container = st.container()

with container:
    entry = service.get_all()
    if name not in entry:
        st.error("Δεν υπάρχει LLM με αυτό το όνομα.")
        st.stop()

    st.html("Είστε σίγουροι ότι θέλετε να διαγράψετε το LLM με όνομα: <b>" + name + "</b>;")
    
    if container.button("Διαγραφή"):
        st.toast("Η διαγραφή του μοντέλου ξεκίνησε, παρακαλώ περιμένετε...", icon=":material/delete:")
        result = service.remove_model(name)
        
        if result:
            st.success("Το LLM διαγράφηκε επιτυχώς.")
            st.switch_page("crud/pages/llm/all_llms.py")
        else:
            st.error("Αποτυχία διαγραφής του LLM.")