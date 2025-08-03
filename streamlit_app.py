import streamlit as st
from mirror_ui import render_mirror_ui

st.set_page_config(page_title="MirrorGPT v0.3", layout="wide")

st.title("🪞 MirrorGPT v0.3 — DiegoSeed")

# Tabbed interface
tabs = st.tabs(["🤖 Chatbot", "🪞 Mirror System"])

with tabs[0]:
    st.info("🤖 *Chatbot UI placeholder coming soon.*")
    st.text_input("Talk to the model:", key="chat_input")
    st.write("Future: This will be connected to GPT via API or local inference.")

with tabs[1]:
    render_mirror_ui()
