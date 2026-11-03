# Η σελίδα επιτρέπει τη διαγραφή ενός Process με βάση το ID του.
from crud.services.ProcessesService import ProcessesService

import streamlit as st

id = st.query_params['id'] if st.query_params['id'] else None
if not id:
    st.error("Λείπει το ID του Process")
    st.stop()

service = ProcessesService()

st.header("Διαγραφή Process")

global container
container = st.container()

with container:
    entry = service.get_by_id(id)
    if isinstance(entry, dict) and "error" in entry:
        container.error(f"Σφάλμα: {entry['error']}")
        st.stop()

    container.html("Είστε σίγουροι ότι θέλετε να διαγράψετε το Process με port: <b>" + str(entry['port']) + "</b>;")
    
    if container.button("Διαγραφή"):
        if entry.get('pid'):
            result = service.delete_process(entry.get('pid'))
            if result and 'error' in result:
                container.error(f"Σφάλμα κατά τον τερματισμό της διεργασίας: {result['error']}")
                st.stop()

        result = service.delete(id)
        
        if result and 'error' in result:
            container.error(f"Σφάλμα κατά τη διαγραφή του Process: {result['error']}")
        else:
            st.switch_page("crud/pages/process/all_processes.py", query_params={"agent_id": entry.get('agent_id')})