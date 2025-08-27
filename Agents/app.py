import streamlit as st
from SearchandCodingAgent import create_agent_and_thread, create_message_and_getreply, delete_agent

st.set_page_config(page_title="Coding Agent", page_icon="🤖")
st.title("Coding Agent")
st.write("Welcome to Coding Agent! Your assistant for coding tasks.")

if "agent" not in st.session_state:
    st.session_state.agent, st.session_state.thread = create_agent_and_thread()
    st.write("Agent and thread created successfully!")

if st.button("End Session"):
    if st.session_state.agent:
        deleted = delete_agent(st.session_state.agent)
        if deleted:
            st.write("Agent session ended and resources cleaned up.")
        else:
            st.write("Failed to delete agent. Please check logs.")
    else:
        st.write("No active agent session to end.")

# Example input box
user_input = st.text_area("Describe your task:")

if st.button("Submit"):
    response = create_message_and_getreply(st.session_state.agent, st.session_state.thread, user_input)
    st.write(f"Agent response: {response}")
    #st.write(f"You entered: {user_input}")


