import streamlit as st
import json
from agents.context_reader import context_reader
from agents.purpose_generator import generate_purpose_statement
from agents.flow_planner import generate_project_flow
from agents.diagram_generator import generate_mermaid_diagram
from agents.feedback_agent import generate_feedback
import streamlit.components.v1 as components

st.set_page_config(page_title="Agentic AI System", layout="centered")

st.title("🤖 Agentic AI System")
st.markdown("Guide your AI project from idea to milestones using GPT-powered agents via OpenRouter.")

# Initialize session state
for key in ["summary", "purpose", "flow", "diagram", "feedback"]:
    if key not in st.session_state:
        st.session_state[key] = ""

# Input fields
project_title = st.text_input("📌 Project Title")
user_goals = st.text_area("🎯 User Goals")
feedback_notes = st.text_area("🗒️ User Feedback Notes")

# Generate Context Summary
if st.button("Generate Context Summary"):
    if not all([project_title, user_goals, feedback_notes]):
        st.warning("Please fill in all the fields.")
    else:
        with st.spinner("🔍 Reading project context..."):
            st.session_state.summary = context_reader(project_title, user_goals, feedback_notes)
        st.success("✅ Context Summary Generated:")

# Display Summary
if st.session_state.summary:
    st.markdown(st.session_state.summary)

    if st.button("Generate Purpose Statement"):
        with st.spinner("✍️ Writing purpose statement..."):
            st.session_state.purpose = generate_purpose_statement(st.session_state.summary)
        st.success("✅ Purpose Statement Generated:")

# Display Purpose
if st.session_state.purpose:
    st.markdown(f"📝 **{st.session_state.purpose}**")

    if st.button("Generate Process Flow"):
        with st.spinner("🧠 Designing project milestones..."):
            st.session_state.flow = generate_project_flow(st.session_state.purpose)
        st.success("✅ Process Flow Plan:")

# Display Flow
if st.session_state.flow:
    st.markdown(st.session_state.flow)

    if st.button("Generate Diagram"):
        with st.spinner("🖼️ Generating visual diagram..."):
            st.session_state.diagram = generate_mermaid_diagram(st.session_state.flow)
        st.success("✅ MermaidJS Diagram Code:")
        st.code(st.session_state.diagram, language="mermaid")

        st.markdown("🔗 [Open in Mermaid Live Editor](https://mermaid.live/edit)")

        if st.session_state.diagram:
            html = f"""
            <script type="module">
              import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';
              mermaid.initialize({{ startOnLoad: true }});
            </script>
            <div class="mermaid">
            {st.session_state.diagram}
            </div>
            """
            components.html(html, height=500, scrolling=True)

# AI Feedback Agent
if st.session_state.flow and st.button("🧪 Get AI Feedback"):
    with st.spinner("Reviewing your project..."):
        st.session_state.feedback = generate_feedback(
            st.session_state.summary,
            st.session_state.purpose,
            st.session_state.flow
        )
    st.success("✅ AI Feedback:")
    st.markdown(st.session_state.feedback)

# Export JSON
if st.session_state.flow and st.button("📥 Export as JSON"):
    export_data = {
        "project_title": project_title,
        "user_goals": user_goals,
        "feedback_notes": feedback_notes,
        "context_summary": st.session_state.summary,
        "purpose_statement": st.session_state.purpose,
        "process_flow": st.session_state.flow,
        "diagram_code": st.session_state.diagram
    }
    json_str = json.dumps(export_data, indent=2)
    st.download_button("Download JSON", data=json_str, file_name="agentic_project.json", mime="application/json")
