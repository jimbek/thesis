import streamlit as st

st.header("Add New REST API")
st.text_input("API Name")
st.text_area("API Description")
st.text_input("API Endpoint")
st.selectbox("HTTP Method", ["GET", "POST", "PUT", "DELETE"])
st.button("Save")