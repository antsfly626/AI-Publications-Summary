import streamlit as st

st.set_page_config(
    page_title="NASA Research Dashboard",
    page_icon="🚀",
    layout="wide",
)

st.title("🚀 NASA Research Paper Dashboard")
st.markdown("""
Welcome! Use the sidebar to navigate between:
- **Select Paper**
- **Describe Paper**
- **Connect Paper**
- **Chatbot (RAG)**
""")

st.image("https://www.nasa.gov/sites/default/files/thumbnails/image/nasa-logo-web-rgb.png", width=200)
