import streamlit as st
from pipeline_graph import build_graph
from export_to_pdf import PDFExporter
import base64

st.set_page_config(page_title="Agentic AI Planner", layout="centered")

st.markdown(
    """
    <style>
        .title-style {
            font-size: 2.5rem;
            font-weight: bold;
            color: #00BFFF;
            text-align: center;
        }
        .stButton>button {
            background-color: #00BFFF;
            color: white;
            border-radius: 8px;
            padding: 10px 24px;
            font-weight: 600;
            font-size: 16px;
        }
        .stTextInput, .stTextArea {
            background-color: #1e1e1e !important;
            color: white !important;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown('<div class="title-style">🚀 Agentic AI Planner ></div>', unsafe_allow_html=True)
st.markdown("### Build high-performance academic or business planners using AI-powered workflows.")

# Sidebar with presets
st.sidebar.header("🧠 Quick Start Presets")
preset_options = {
    "None": {},
    "Academic Planner": {
        "title": "AI-Powered Academic Planner",
        "goals": "Help students generate structured project plans",
        "feedback": "Should be fast, visual, and helpful"
    },
    "Business Insight Tool": {
        "title": "AI-Powered Market Insight Generator",
        "goals": "Help startups analyze competitors and generate product-market fit strategies using AI",
        "feedback": "Should deliver strategic insights, identify trends, and visualize opportunities"
    },
    "Study Tracker": {
        "title": "Smart Study Tracker",
        "goals": "Motivate students with AI reminders and gamified tasks",
        "feedback": "Should use smart nudges, visualize progress, and give rewards"
    }
}

preset = st.sidebar.selectbox("Choose a preset", list(preset_options.keys()))
prefill = preset_options.get(preset, {})

# Inputs
with st.form("ai_plan_form"):
    st.subheader("🔧 Enter Your Project Info")
    title = st.text_input("📘 Project Title", prefill.get("title", ""))
    goals = st.text_area("🎯 Project Goals", prefill.get("goals", ""))
    feedback = st.text_area("💬 Feedback Requirements", prefill.get("feedback", ""))
    submitted = st.form_submit_button("✨ Generate Plan")

# Processing
if submitted:
    if not title or not goals:
        st.warning("Please fill in both Title and Goals.")
    else:
        with st.spinner("⏳ Thinking like Gemini..."):
            graph = build_graph()
            result = graph.invoke({
                "title": title,
                "goals": goals,
                "feedback": feedback
            })

        st.success("🎉 Plan generated successfully!")

        # Tabs for clean output
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "🎯 Purpose", "🪜 Flow", "📈 Diagram", "🧠 Feedback", "🌍 Market Insights"
        ])

        with tab1:
            st.markdown(result.get("purpose", ""))

        with tab2:
            st.markdown(result.get("flow", ""))

        with tab3:
            st.markdown("```mermaid\n" + result.get("diagram", "").strip("```") + "\n```")

        with tab4:
            st.markdown(result.get("feedback_out", ""))

        with tab5:
            st.markdown(result.get("market_insights", ""))

        # ✅ Export to PDF
        pdf_filename = "AI_Project_Report.pdf"
        exporter = PDFExporter(result)
        exporter.export(pdf_filename)

        # ✅ PDF download button
        with open(pdf_filename, "rb") as pdf_file:
            base64_pdf = base64.b64encode(pdf_file.read()).decode("utf-8")
            download_link = f'<a href="data:application/pdf;base64,{base64_pdf}" download="{pdf_filename}">📥 Download PDF Report</a>'
            st.markdown("### 📄 Export", unsafe_allow_html=True)
            st.markdown(download_link, unsafe_allow_html=True)
