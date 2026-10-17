# This page displays the list of existing LLMs.
from crud.services.Ollama import OllamaService

import streamlit as st

service = OllamaService()

# Initialize a container for the page content.
global container
container = st.container()

with container:
    container.markdown(
        """
            <style>
                .st-emotion-cache-r6kf2v {
                    max-width: 90%;
                }

                .st-emotion-cache-uvlrfw {
                    width: 0;
                    max-width: 0;
                }
            </style>
        """,
        unsafe_allow_html=True,
    )

    container.header("LLMs", divider="gray")
    
    if container.button("New +", type="primary"):
        st.switch_page("crud/pages/llm/add_llm.py")

    header = container.columns([2, 0.5])
    header[0].markdown("**Όνομα**")
    header[1].markdown("**Ενέργειες**")

    for llm in service.get_all():
        row = container.columns([2, 0.5])

        row[0].markdown(llm)

        action_buttons = row[1].columns(1)
        action_buttons[0].page_link(
            "crud/pages/llm/delete_llm.py",
            label = "",
            icon = ":material/delete:",
            query_params = {"name": llm})