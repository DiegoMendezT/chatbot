import streamlit as st
from mirror_ui import render_mirror_ui
from mirror_echo import EchoSurge

st.set_page_config(page_title="MirrorGPT v0.6", layout="wide")

# Initialize EchoSurge in session state
if 'echo_surge' not in st.session_state:
    st.session_state.echo_surge = EchoSurge()

echo_surge = st.session_state.echo_surge

st.title("🪞 MirrorGPT v0.6 — EchoSurge")

# Sidebar for persona selection and sync log
with st.sidebar:
    st.header("Inner Council")
    
    persona_list = list(echo_surge.personas.keys())
    selected_persona = st.selectbox(
        "Select Persona",
        options=persona_list,
        index=persona_list.index(echo_surge.active_persona)
    )

    if selected_persona != echo_surge.active_persona:
        echo_surge.set_persona(selected_persona)
        st.rerun()

    with st.expander("📈 Live Sync Log"):
        st.write(echo_surge.get_log_entries())

# Tabbed interface
tabs = st.tabs(["🤖 Chatbot", "🪞 Mirror System"])

with tabs[0]:
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Pre-seed the conversation
    if not st.session_state.messages:
        st.session_state.messages.append({"role": "assistant", "content": "What reflection are you seeking today?"})

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Accept user input
    if prompt := st.chat_input("What is up?"):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(prompt)

        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = echo_surge.generate_response(prompt)
            message_placeholder.markdown(full_response)
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": full_response})

with tabs[1]:
    render_mirror_ui()
