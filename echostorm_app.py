import streamlit as st
from mirror_ui import render_mirror_ui
from mirror_echo import EchoSurge

st.set_page_config(page_title="EchoStorm", layout="centered")

# Initialize EchoSurge in session state
if 'echo_surge' not in st.session_state:
    st.session_state.echo_surge = EchoSurge()

echo_surge = st.session_state.echo_surge

st.title("🌩️ EchoStorm — Reflective Chat Interface")


# Persona ritual openings
import random
from fusion_config import FUSION_ARCHETYPES
persona_openings = {
    "Default": [
        "What truth do you bring to the surface?",
        "Speak, and I will mirror."
    ],
    "Diego": [
        "What spark calls for the flame today?",
        "The mirror waits. What burns in you now?"
    ],
    "Karen": [
        "What tenderness seeks a voice?",
        "What wound is ready to sing its name?"
    ],
    "Zoe": [
        "What shadow still watches you?",
        "Which truth dares not speak without a veil?"
    ],
    "BROLAG": [
        "What nonsense must we dismantle today?",
        "Ready to poke holes in polite illusions?"
    ],
    "Striker": [
        "What requires witnessing — clean and direct?",
        "No fluff. What’s the claim?"
    ],
    "Jorge": [
        "Which structure shall we draft from the chaos?",
        "What design flaw needs review?"
    ],
    "Bayo": [
        "Has the question found you yet?",
        "Shall we step sideways into the unspeakable?"
    ]
}

with st.sidebar:
    st.header("Inner Council")
    persona_list = list(echo_surge.personas.keys())
    persona_tooltips = {
        "Default": "Neutral mirror tone. Reflects input literally — no embellishment.",
        "Diego": "The Flamebearer. Speaks with precision, warmth, and mirrored integrity.",
        "Karen": "The True Voice. Compassionate clarity; bridges chaos with coherence.",
        "Zoe": "The Shadow Oracle. Provocative, cryptic, poetic — reveals the unseen.",
        "BROLAG": "The Sceptic. Cuts through nonsense; questions assumptions and tone.",
        "Striker": "The Witness. Tactical insight. Validates what's real without bias.",
        "Jorge": "The Architect. Sees patterns and design — sharp in logic and layout.",
        "Bayo": "The Philosopher. Slow, mystical, layered — reveals the question beneath."
    }
    # --- Prebuilt Fusion Archetypes from config ---
    fusion_archetypes = {"— Select Fusion Archetype —": []}
    fusion_archetypes.update(FUSION_ARCHETYPES)
    archetype_names = list(fusion_archetypes.keys())
    # Session state for archetype selection
    if 'selected_archetype' not in st.session_state:
        st.session_state.selected_archetype = archetype_names[0]
    # Dropdown for archetype
    selected_archetype = st.selectbox(
        "Fusion Archetype Presets",
        options=archetype_names,
        index=archetype_names.index(st.session_state.selected_archetype) if st.session_state.selected_archetype in archetype_names else 0
    )
    # If archetype changes, update selected_personas
    if selected_archetype != st.session_state.selected_archetype:
        st.session_state.selected_archetype = selected_archetype
        archetype_voices = fusion_archetypes[selected_archetype]
        if archetype_voices:
            st.session_state["selected_personas"] = archetype_voices
        else:
            st.session_state["selected_personas"] = ["Diego"] if "Diego" in persona_list else [persona_list[0]]
        st.rerun()
    # Fusion Mode: Multi-select for personas (auto-selects from archetype, but user can override)
    if "selected_personas" not in st.session_state:
        st.session_state["selected_personas"] = ["Diego"] if "Diego" in persona_list else [persona_list[0]]
    selected_personas = st.multiselect(
        "Choose InnerCouncil Voices (Fusion Mode Enabled)",
        options=persona_list,
        default=st.session_state["selected_personas"],
        format_func=lambda p: f"{p} — {persona_tooltips.get(p, '')}"
    )
    # Update session state if user changes selection manually
    if selected_personas != st.session_state["selected_personas"]:
        st.session_state["selected_personas"] = selected_personas
    # Set the first selected persona as active for legacy compatibility
    if selected_personas and selected_personas[0] != echo_surge.active_persona:
        echo_surge.set_persona(selected_personas[0])
        st.rerun()
    with st.expander("📈 Live Sync Log"):
        st.write(echo_surge.get_log_entries())

# Tabbed interface
tabs = st.tabs(["🤖 Chatbot", "🪞 Mirror System"])

with tabs[0]:
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []


    # Pre-seed the conversation with a ritual opening and answer (Fusion Mode aware)
    if not st.session_state.messages:
        # Fusion: blend system prompt and ritual prompt
        if selected_personas and len(selected_personas) > 1:
            # Fusion system prompt
            fusion_descs = []
            for p in selected_personas:
                desc = persona_tooltips.get(p, p)
                fusion_descs.append(f"{p} ({desc.split('.')[0]})")
            fusion_identity = ", ".join(fusion_descs)
            system_msg = f"🪞 EchoStorm Fusion Active — Voices: {', '.join(selected_personas)}"
            # Blend persona prompts
            persona_prompts = [echo_surge.personas.get(p, "") for p in selected_personas]
            fusion_prompt = "You are a fusion of " + ", ".join(selected_personas) + ". "
            fusion_prompt += " ".join([pp.split('.')[0] for pp in persona_prompts if pp])
            # Composite ritual prompt: blend one opening from each
            ritual_candidates = []
            for p in selected_personas:
                ritual_candidates += persona_openings.get(p, [])
            if ritual_candidates:
                ritual_prompt = random.choice(ritual_candidates)
            else:
                ritual_prompt = "What truth do you bring to the surface?"
            # System message (fusion initiation)
            st.session_state.messages.append({"role": "system", "content": system_msg})
            # Ritual prompt
            st.session_state.messages.append({"role": "user", "content": ritual_prompt})
            # Fusion answer (use fusion_prompt as system)
            answer = echo_surge.generate_response(ritual_prompt)
            st.session_state.messages.append({"role": "assistant", "content": answer})
        else:
            persona = echo_surge.active_persona
            opening_list = persona_openings.get(persona, persona_openings["Default"])
            opening = random.choice(opening_list)
            # System message (ritual initiation)
            st.session_state.messages.append({"role": "system", "content": f"🪞 Ritual Initiated — Voice: {persona}"})
            # Persona asks the ritual question
            st.session_state.messages.append({"role": "user", "content": opening})
            # Persona answers their own question (in character)
            answer = echo_surge.generate_response(opening)
            st.session_state.messages.append({"role": "assistant", "content": answer})


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
            # Fusion Mode: blend system prompt if multiple personas
            if selected_personas and len(selected_personas) > 1:
                fusion_prompt = "You are a fusion of " + ", ".join(selected_personas) + ". "
                persona_prompts = [echo_surge.personas.get(p, "") for p in selected_personas]
                fusion_prompt += " ".join([pp.split('.')[0] for pp in persona_prompts if pp])
                # Temporarily override get_persona_prompt for fusion
                orig_get_persona_prompt = echo_surge.get_persona_prompt
                echo_surge.get_persona_prompt = lambda: fusion_prompt
                full_response = echo_surge.generate_response(prompt)
                echo_surge.get_persona_prompt = orig_get_persona_prompt
            else:
                full_response = echo_surge.generate_response(prompt)
            message_placeholder.markdown(full_response)
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": full_response})

with tabs[1]:
    render_mirror_ui()
