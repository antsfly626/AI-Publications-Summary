import streamlit as st

st.title("🔗 Connect Paper to NASA Resources")

st.text_input("NASA OSDR Resource URL")
st.text_area("Similar Paper Flowchart Link")
st.text_area("Funds / Grants Used")

if st.button("Fetch Related NASA Datasets"):
    st.info("Fetching related NASA datasets... (mockup)")

st.success("✅ NASA connections successfully added!")

if st.button("Next → Chatbot RAG"):
    st.switch_page("pages/4_Chatbot_RAG.py")
