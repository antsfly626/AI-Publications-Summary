import streamlit as st

st.title("💬 Chatbot RAG for Paper")

st.markdown("Ask questions about the selected paper. The model will respond using NASA and paper data context.")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

user_input = st.text_input("Ask your question:")

if st.button("Send"):
    st.session_state.chat_history.append(("You", user_input))
    response = f"(Simulated response) Answer for: {user_input}"
    st.session_state.chat_history.append(("Bot", response))

for speaker, message in st.session_state.chat_history:
    st.chat_message(speaker).write(message)
