# Η σελίδα επιτρέπει την απεγκατάσταση ενός LLM.
from crud.services.LLMsService import LLMsService

import streamlit as st

name = st.query_params['name'] if st.query_params['name'] else None
if not name:
    st.error("Λείπει το όνομα του LLM")
    st.stop()

service = LLMsService()

st.header("Διαγραφή LLM", divider="gray")

global container
container = st.container()

with container:
    entry = service.get_all()
    if name not in entry:
        st.error("Δεν υπάρχει LLM με αυτό το όνομα.")
        st.stop()

    st.html("Είστε σίγουροι ότι θέλετε να διαγράψετε το LLM με όνομα: <b>" + name + "</b>;")
    st.info("Η διαδικασία διαγραφής του μοντέλου μπορεί να διαρκέσει μερικά δευτερόλεπτα.")
    
    if container.button("Διαγραφή"):
        st.toast("Η διαγραφή του μοντέλου ξεκίνησε, παρακαλώ περιμένετε...", icon=":material/delete:")
        result = service.remove_model(name)
        
        if result:
            st.success("Το LLM διαγράφηκε επιτυχώς.")
            st.switch_page("crud/pages/llm/all_llms.py")
        else:
            st.error("Αποτυχία διαγραφής του LLM.")