# Η σελίδα επιτρέπει την προσθήκη νέου Process.
from crud.services.ProcessesService import ProcessesService
from crud.services.AgentsService import AgentsService
from crud.services.LLMsService import LLMsService

import streamlit as st

agent_id = st.query_params['agent_id'] if st.query_params['agent_id'] else None
if not agent_id:
    st.error("Λείπει το ID του AI Agent")
    st.stop()

service = ProcessesService()
agent_service = AgentsService()
llms_service = LLMsService()

st.header("Προσθήκη Process")

global container
container = st.container()

with container:
    agent = agent_service.get_by_agent_id(agent_id)
    if isinstance(agent, dict) and "error" in agent:
        container.error(f"Σφάλμα: {agent['error']}")
        st.stop()
    
    port = container.number_input("Port", min_value=8000)

    all_llms = llms_service.get_all()
    llm = container.selectbox(
        "LLM",
        options=[None] + [llm for llm in all_llms],
        format_func=lambda name: "None" if name is None else next(llm for llm in all_llms if llm == name)
    )

    if container.button("Save"):
        if not llm:
            st.toast("Πρέπει να επιλέξετε ένα LLM.")
            st.stop()
        
        payload = {
            "port": port,
            "system_prompt": agent.get('system_prompt'),
            "llm": llm,
            "mcp_server_ids": agent.get('mcp_server_ids')
        }
        
        result = service.run_process(payload)
        if isinstance(result, dict) and "error" in result:
            container.error(f"Σφάλμα: {result['error']}")
            st.stop()

        data = {
            "pid": result.get('pid'),
            "llm": llm,
            "agent_id": agent_id,
            "port": port
        }

        result = service.add(data)
        if isinstance(result, dict) and "error" in result:
            service.delete_process(data['pid'])
            container.error(f"Σφάλμα: {result['error']}")
            st.stop()
        else:
            st.switch_page("crud/pages/process/all_processes.py", query_params={"agent_id": agent_id})