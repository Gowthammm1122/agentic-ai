import streamlit as st
from pipeline_graph import build_graph
from export_to_pdf import PDFExporter
import base64
import os
import shutil
from dotenv import load_dotenv

# Load env vars at the start
load_dotenv()

# --- CONFIG & STYLING ---
st.set_page_config(page_title="Agentic AI Planner Pro", layout="wide", page_icon="🚀")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    .main {
        background: radial-gradient(circle at top right, #1e293b, #0f172a);
    }
    
    .stApp {
        background: transparent;
    }

    .title-container {
        padding: 2rem 0;
        text-align: center;
        background: rgba(255, 255, 255, 0.03);
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        margin-bottom: 2rem;
    }

    .title-style {
        font-size: 3.5rem;
        font-weight: 800;
        background: linear-gradient(90deg, #38bdf8, #818cf8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }

    .subtitle-style {
        color: #94a3b8;
        font-size: 1.2rem;
    }

    .card {
        background: rgba(255, 255, 255, 0.05);
        padding: 1.5rem;
        border-radius: 15px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        margin-bottom: 1rem;
    }

    .stButton>button {
        width: 100%;
        background: linear-gradient(90deg, #0ea5e9, #2563eb) !important;
        color: white !important;
        border: none !important;
        padding: 0.8rem !important;
        font-weight: 700 !important;
        border-radius: 10px !important;
        transition: all 0.3s ease !important;
    }

    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(14, 165, 233, 0.4);
    }

    .agent-log {
        font-family: 'Courier New', Courier, monospace;
        background: #000;
        color: #0f0;
        padding: 10px;
        border-radius: 5px;
        font-size: 0.8rem;
        max-height: 200px;
        overflow-y: auto;
        margin-bottom: 1rem;
    }
    </style>
""", unsafe_allow_html=True)

# --- SIDEBAR & UTILS ---
with st.sidebar:
    st.image("https://img.icons8.com/isometric/512/artificial-intelligence.png", width=100)
    st.header("⚙️ Control Panel")
    
    if st.button("🔥 Clear Agent Cache"):
        if os.path.exists(".agent_cache"):
            shutil.rmtree(".agent_cache")
        st.success("Cache Cleared!")
        st.rerun()

    st.divider()
    st.header("🧠 Quick Start Presets")
    preset_options = {
        "None": {},
        "Academic Planner": {
            "title": "AI-Powered Academic Planner",
            "goals": "Help students generate structured project plans and study schedules",
            "feedback": "Focus on academic rigour and clear milestones"
        },
        "Business Insight Tool": {
            "title": "Market Disruptor Insight Generator",
            "goals": "Identify gaps in the SaaS market for small businesses",
            "feedback": "Needs sharp competitive analysis and go-to-market strategies"
        }
    }
    preset = st.selectbox("Choose a preset", list(preset_options.keys()))
    prefill = preset_options.get(preset, {})

# --- MAIN UI ---
st.markdown('<div class="title-container"><div class="title-style">Agentic AI Planner Pro</div><div class="subtitle-style">Premium Multi-Agent Orchestration with Self-Correction</div></div>', unsafe_allow_html=True)

col1, col2 = st.columns([1, 2])

with col1:
    with st.form("ai_plan_form"):
        st.subheader("🔧 Project Definition")
        title = st.text_input("📘 Project Title", prefill.get("title", ""))
        goals = st.text_area("🎯 Core Goals", prefill.get("goals", ""), height=100)
        feedback = st.text_area("💬 Specific Requirements", prefill.get("feedback", ""), height=80)
        submitted = st.form_submit_button("✨ Orchestrate Agents")

with col2:
    if submitted:
        if not title or not goals:
            st.error("Please provide both a Title and Goals to start the orchestration.")
        else:
            log_container = st.empty()
            progress_bar = st.progress(0)
            
            # Simulated logs for transparency
            logs = ["Initializing Agentic State...", "Starting context reader..."]
            log_container.markdown(f'<div class="agent-log">{"<br>".join(logs)}</div>', unsafe_allow_html=True)
            
            graph = build_graph()
            
            with st.spinner("🤖 Agents are collaborating (Self-Correction enabled)..."):
                # Run graph
                result = graph.invoke({
                    "title": title,
                    "goals": goals,
                    "feedback": feedback
                })
                
                # Update logs based on result (simulated sequence for effect)
                logs.append(f"Context captured. (Retries: {result.get('retry_count', 0)})")
                if result.get("review_result") and "APPROVED" in result["review_result"].upper():
                    logs.append("✅ Reviewer: Plan approved on first pass.")
                else:
                    logs.append("⚠️ Reviewer: Detected gaps. Self-corrected plan.")
                logs.append("Finalizing insights and diagrams...")
                log_container.markdown(f'<div class="agent-log">{"<br>".join(logs)}</div>', unsafe_allow_html=True)
                progress_bar.progress(100)

            st.success("🎉 Full Orchestration Complete!")

            # Tabs for output
            tab1, tab2, tab3, tab4, tab5 = st.tabs([
                "🎯 Strategy", "🪜 Execution Flow", "📊 Architecture", "🧠 Expert Critique", "🌍 Market Intelligence"
            ])

            with tab1:
                st.markdown(result.get("purpose", ""))

            with tab2:
                st.markdown(result.get("flow", ""))

            with tab3:
                diag = result.get("diagram", "").strip()
                if diag:
                    # Strip markdown blocks if present
                    diag = diag.replace("```mermaid", "").replace("```", "").strip()
                    st.markdown(f"```mermaid\n{diag}\n```")
                else:
                    st.info("No diagram generated.")

            with tab4:
                st.markdown(result.get("feedback_out", ""))

            with tab5:
                st.markdown(result.get("market_insights", ""))

            # --- EXPORT ---
            st.divider()
            col_a, col_b = st.columns([1, 1])
            with col_a:
                pdf_filename = "AI_Strategic_Plan.pdf"
                exporter = PDFExporter(result)
                exporter.export(pdf_filename)

                with open(pdf_filename, "rb") as f:
                    base_64_pdf = base64.b64encode(f.read()).decode('utf-8')
                    pdf_display = f'<a href="data:application/pdf;base64,{base_64_pdf}" download="{pdf_filename}" style="text-decoration:none;"><div style="background-color:#2563eb;color:white;padding:10px;border-radius:10px;text-align:center;font-weight:bold;">📥 Download PDF Strategic Report</div></a>'
                    st.markdown(pdf_display, unsafe_allow_html=True)
            
            with col_b:
                st.info("💡 **Tip:** Clear the Agent Cache in the sidebar if you change your goals significantly to get fresh AI perspectives.")
    else:
        st.info("👈 Fill out the project details and click 'Orchestrate Agents' to begin.")
        st.image("https://images.unsplash.com/photo-1677442136019-21780ecad995?auto=format&fit=crop&q=80&w=1000", caption="Powered by Gemini 1.5 & LangGraph")
