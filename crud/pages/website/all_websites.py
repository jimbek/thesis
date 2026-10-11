# This is the page that displays all websites.
import streamlit as st

# Initialize a container for the page content.
global container
container = st.container(horizontal=True)

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

    left, right = st.columns(2)
    with left:
        container.header("Websites", divider="gray")
    with right:
        if container.button("New +", type="primary"):
            st.switch_page("crud/pages/website/add_website.py")