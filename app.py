import streamlit as st
from agent import chat_with_agent

st.set_page_config(page_title='Travelling Agent')

st.title('Travel Planning Agent')


# Chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


# Chat input
user_input = st.chat_input("Enter your travel query...")

if user_input:
    # Save user message
    st.session_state.chat_history.append(
        {
            "role": "user",
            "content": user_input
        }
    )

    # Get AI response
    response = chat_with_agent(user_input)

    # Save AI response
    st.session_state.chat_history.append(
        {
            "role": "assistant",
            "content": response
        }
    )


# Display chat history
for msg in st.session_state.chat_history:

    with st.chat_message(msg["role"]):
        st.write(msg["content"])