# This page allows the user to chat with an AI Agent through a specific Process.
from crud.services.ProcessesService import ProcessesService

import streamlit as st

id = st.query_params['id'] if st.query_params['id'] else None
if not id:
    st.error("Λείπει το ID του Process")
    st.stop()

service = ProcessesService()

st.header("Chat με AI Agent μέσω Process")

# Initialize a container for the page content.
global container
container = st.container()

with container:
    entry = service.get_by_id(id)
    if isinstance(entry, dict) and "error" in entry:
        container.error(f"Σφάλμα: {entry['error']}")
        st.stop()

    # Χρησιμοποιούμε cache για να κρατάμε τη λίστα ζωντανή όσο τρέχει η σελίδα
    @st.cache_resource
    def get_chat_history():
        # Αυτό θα τρέξει ΜΟΝΟ την πρώτη φορά που θα φορτώσει η σελίδα
        return []

    # Μια απλή, κανονική λίστα Python που "επιβιώνει" από τα re-runs
    history = get_chat_history()

    # Εμφάνιση των μηνυμάτων
    for message in history:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    # Λήψη νέου μηνύματος
    if user_input := st.chat_input("Γράψτε εδώ..."):
        
        # Εμφάνιση και προσθήκη του χρήστη στη λίστα
        with st.chat_message("user"):
            st.write(user_input)
        history.append({"role": "user", "content": user_input})
        
        # Απάντηση Agent
        with st.chat_message("agent"):
            try:
                # Αντικαταστήστε με τη δυναμική θύρα που χρησιμοποιεί το Flask σας
                response = service.chat({ "port": entry['port'], "message": user_input})
                agent_reply = "Η επικοινωνία με τον AI Agent απέτυχε: " + response["error"] if isinstance(response, dict) and "error" in response else response
            except Exception as e:
                agent_reply = f"Σφάλμα σύνδεσης με τον Agent: {e}"
            st.write(agent_reply)
        
        # Προσθήκη της απάντησης στη λίστα
        history.append({"role": "agent", "content": agent_reply})