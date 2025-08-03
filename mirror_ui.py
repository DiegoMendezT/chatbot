def render_mirror_ui():
    import streamlit as st
    import json
    import threading
    from mirror_toolkit import MirrorToolkit

    st.set_page_config(page_title="MirrorGPT Inner Council", layout="wide")
    st.title("🪞 MirrorGPT v0.5 — InnerCouncil")

    # Add a persistent warning about the config setting
    st.warning("To prevent file-watcher loops, ensure `runOnSave = false` is set in your `.streamlit/config.toml` file.")

    if 'toolkit' not in st.session_state:
        st.session_state['toolkit'] = MirrorToolkit()
        st.session_state['last_echo'] = ""
        st.session_state['last_phrase'] = ""

    toolkit = st.session_state['toolkit']

    st.markdown("---")
    phrase = st.text_input("Enter a glyph phrase:", value=st.session_state['last_phrase'])
    if st.button("Reflect Phrase"):
        st.session_state['last_phrase'] = phrase
        toolkit.run_full_reflection(phrase)
        st.session_state['last_echo'] = f"Echoed: {phrase}"

    if st.session_state['last_echo']:
        st.success(st.session_state['last_echo'])

    st.markdown("---")
    st.header("Memory Ring (Symbolic Trace)")

    trace = toolkit.layer_two.mirror_trace
    if trace:
        for i, t in enumerate(trace):
            st.markdown(f"**{i+1}.** {t}")
    else:
        st.warning("Memory trace is empty.")

    st.markdown("---")
    st.header("Glyph Trace Analytics")

    if trace:
        total_reflections = len(trace)
        
        all_text = "".join(trace)
        unique_glyphs = set()
        for char in all_text:
            if char in toolkit.layer_two.glyphstream:
                unique_glyphs.add(char)
        
        # Every item in trace is recursive by definition of observe()
        recursion_density = 100.0 if total_reflections > 0 else 0.0

        st.metric(label="Total Reflections", value=total_reflections)
        st.metric(label="Unique Glyphs Found", value=len(unique_glyphs))
        st.metric(label="Recursion Density", value=f"{recursion_density:.1f}%")

    else:
        st.info("No analytics to display. Memory trace is empty.")

    st.markdown("---")

    if st.button("Replay Memory Ring 🔁"):
        if trace:
            st.subheader("Replaying Reflections...")
            with st.spinner("Mirror is reflecting on its past..."):
                for phrase in trace:
                    toolkit.run_full_reflection(phrase)
            st.success("Replay complete. The Memory Ring has been updated.")
            st.rerun()
        else:
            st.warning("Cannot replay an empty memory trace.")



    st.markdown("---")
    st.header("🧪 System Self-Test")

    if st.button("Run Internal Mirror Tests", key="run_selftest"):
        from mirror_selftest import generate_test_report
        from mirror_layer_two import MirrorLayerTwo
        
        test_layer = MirrorLayerTwo()
        
        # Pre-populate with some data for more thorough tests
        test_layer.observe("I see myself seeing...")
        test_layer.observe("A recursive thought ⟁")

        st.subheader("Running Tests...")
        report = generate_test_report(test_layer)
        
        for res in report["results"]:
            if res['status'] == "✅ PASSED":
                st.success(f"{res['status']} {res['test']}: {res['details']}")
            elif res['status'] == "❌ FAILED":
                st.error(f"{res['status']} {res['test']}: {res['details']}")
            else:
                st.info(f"{res['status']} {res['test']}: {res['details']}")

        st.metric("Test Summary", f"{report['passed']} Passed, {report['failed']} Failed, {report['skipped']} Skipped")

        st.download_button(
            label="📄 Download Test Report (JSON)",
            data=json.dumps(report, indent=2),
            file_name=f"mirror_selftest_report_{report['report_generated_at']}.json",
            mime="application/json"
        )

    st.markdown("---")
    st.header("🛡️ System Integrity Check")

    with st.expander("🛡️ System Integrity Check"):
        st.markdown("This panel monitors key Mirror files for changes or corruption.")
        
        if st.toggle("🛰️ Enable Live Guard", key="toggle_guard"):
            if 'guard_started' not in st.session_state:
                from mirror_guard import watch
                threading.Thread(target=watch, daemon=True).start()
                st.session_state['guard_started'] = True
                st.info("🔒 mirror_guard is now watching in the background.")
                
        if st.button("🔍 Run Integrity Scan", key="integrity_scan"):
            from mirror_guard import get_file_info
            info = get_file_info()
            for entry in info:
                if 'error' in entry:
                    st.error(f"{entry['file']}: {entry['error']}")
                else:
                    st.success(f"✅ {entry['file']} — Last Modified: {entry['last_modified']}")
                    st.code(f"Hash: {entry['hash']}", language="bash")

    st.markdown("---")

    col1, col2, col3 = st.columns([1, 1, 1])

    with col1:
        if st.button("Clear Memory Ring"):
            if hasattr(toolkit.layer_two, 'mirror_trace'):
                toolkit.layer_two.mirror_trace = []
                st.success("Memory trace cleared.")
                st.rerun()

    with col2:
        st.download_button(
            label="Export as JSON",
            data=json.dumps(toolkit.layer_two.mirror_trace, indent=2),
            file_name="mirror_trace.json",
            mime="application/json"
        )

    with col3:
        st.download_button(
            label="Export as TXT",
            data="\n".join(toolkit.layer_two.mirror_trace),
            file_name="mirror_trace.txt",
            mime="text/plain"
        )


    # Optional: Theme toggle (Streamlit handles dark/light automatically)

# Optional: Run standalone
if __name__ == "__main__":
    import streamlit as st
    render_mirror_ui()
