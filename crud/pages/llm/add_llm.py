# Η σελίδα επιτρέπει την εγκατάσταση νέου LLM.
from crud.services.LLMsService import LLMsService

import streamlit as st

service = LLMsService()

st.header("Εγκατάσταση LLM", divider="gray")

global container
container = st.container()

with container:
    name = container.text_input("Όνομα", placeholder="llama3.2")

    container.info('''
        Η διαδικασία εγκατάστασης του μοντέλου μπορεί να διαρκέσει αρκετά δευτερόλεπτα, ανάλογα με το μέγεθος του.
        Επισκεφθείτε την ιστοσελίδα https://ollama.com/search για να βρείτε τα διαθέσιμα μοντέλα.
    ''')

    if container.button("Αποθήκευση"):
        if not name:
            container.error("Παρακαλώ εισάγετε το όνομα του μοντέλου.")
            st.stop()

        st.toast("Η εγκατάσταση του μοντέλου ξεκίνησε, παρακαλώ περιμένετε...", icon=":material/download:")
        result = service.download_model(name)
        
        if result:
            st.switch_page("crud/pages/llm/all_llms.py")
        else:
            container.error("Σφάλμα κατά τη λήψη του μοντέλου.")