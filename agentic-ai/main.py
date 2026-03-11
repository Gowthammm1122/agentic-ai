import streamlit as st
from pipeline_graph import build_graph
from export_to_pdf import PDFExporter
import base64
import os
import shutil
from dotenv import load_dotenv

load_dotenv()

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Axon — The intelligence hub",
    layout="wide",
    page_icon="⚡",
)

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;800&display=swap');

    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

    .main  { background: radial-gradient(circle at top right, #1e293b, #0f172a); }
    .stApp { background: transparent; }

    /* ── Title card ── */
    .title-container {
        padding: 2.2rem 0;
        text-align: center;
        background: rgba(255,255,255,0.03);
        border-radius: 20px;
        border: 1px solid rgba(255,255,255,0.1);
        backdrop-filter: blur(10px);
        margin-bottom: 2rem;
    }
    .title-style {
        font-size: 3.2rem;
        font-weight: 800;
        background: linear-gradient(90deg, #38bdf8, #818cf8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.4rem;
    }
    .subtitle-style { color: #94a3b8; font-size: 1.1rem; }

    /* ── Agent log terminal ── */
    .agent-log {
        font-family: 'Courier New', monospace;
        background: #020617;
        color: #4ade80;
        padding: 12px 16px;
        border-radius: 8px;
        border: 1px solid #1e3a5f;
        font-size: 0.78rem;
        max-height: 220px;
        overflow-y: auto;
        margin-bottom: 1rem;
        line-height: 1.6;
    }

    /* ── Status chips ── */
    .chip-approved {
        display: inline-block;
        background: #14532d; color: #4ade80;
        border-radius: 20px; padding: 2px 12px;
        font-size: 0.78rem; font-weight: 700;
    }
    .chip-rejected {
        display: inline-block;
        background: #7f1d1d; color: #fca5a5;
        border-radius: 20px; padding: 2px 12px;
        font-size: 0.78rem; font-weight: 700;
    }
    .chip-info {
        display: inline-block;
        background: #1e3a5f; color: #7dd3fc;
        border-radius: 20px; padding: 2px 12px;
        font-size: 0.78rem; font-weight: 700;
    }

    /* ── Form / buttons ── */
    .stButton > button {
        width: 100%;
        background: linear-gradient(90deg, #0ea5e9, #2563eb) !important;
        color: white !important;
        border: none !important;
        padding: 0.8rem !important;
        font-weight: 700 !important;
        border-radius: 10px !important;
        transition: all 0.3s ease !important;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 14px rgba(14,165,233,0.45);
    }

    /* ── Cards ── */
    .card {
        background: rgba(255,255,255,0.05);
        padding: 1.4rem;
        border-radius: 14px;
        border: 1px solid rgba(255,255,255,0.09);
        margin-bottom: 1rem;
    }
    </style>
""", unsafe_allow_html=True)


# ── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.image("https://img.icons8.com/isometric/512/artificial-intelligence.png", width=90)
    st.header("⚙️ Control Panel")

    if st.button("🔥 Clear Agent Cache"):
        if os.path.exists(".agent_cache"):
            shutil.rmtree(".agent_cache")
        st.success("Cache cleared!")
        st.rerun()

    st.divider()
    st.header("🧠 Quick Presets")
    preset_options = {
        "None": {},
        "Academic Planner": {
            "title": "AI-Powered Academic Planner",
            "goals": "Help students generate structured project plans and study schedules",
            "feedback": "Focus on academic rigour and clear milestones",
        },
        "Business Insight Tool": {
            "title": "Market Disruptor Insight Generator",
            "goals": "Identify gaps in the SaaS market for small businesses",
            "feedback": "Needs sharp competitive analysis and go-to-market strategies",
        },
        "Healthcare AI": {
            "title": "AI Patient Triage Assistant",
            "goals": "Reduce ER wait times by triaging patients using ML symptoms analysis",
            "feedback": "Must be HIPAA-compliant; integrate with EHR systems",
        },
    }
    preset = st.selectbox("Choose a preset", list(preset_options.keys()))
    prefill = preset_options.get(preset, {})

    st.divider()
    st.markdown("### 🔄 Agentic Pipeline")
    st.markdown("""
    ```
    Context Reader
         ↓
    Vision Agent ←──────┐
         ↓              │ REJECTED
    Flow Planner         │ (self-correct)
         ↓              │
    QA Reviewer ────────┘
         ↓ APPROVED
    Diagram Agent
         ↓
    Risk Analyst
         ↓
    Market Intel (RAG)
    ```
    """)


# ── Main UI ────────────────────────────────────────────────────────────────────
st.markdown(
    '<div class="title-container">'
    '<div class="title-style">⚡ Axon</div>'
    '<div class="subtitle-style">Autonomous Multi-Agent Orchestration · Self-Correcting · LangGraph + LangChain · Groq LLaMA</div>'
    '</div>',
    unsafe_allow_html=True,
)

col1, col2 = st.columns([1, 2])

with col1:
    with st.form("ai_plan_form"):
        st.subheader("🔧 Project Definition")
        title    = st.text_input("📘 Project Title",           prefill.get("title", ""))
        goals    = st.text_area("🎯 Core Goals",               prefill.get("goals", ""),    height=110)
        feedback = st.text_area("💬 Specific Requirements",    prefill.get("feedback", ""), height=80)
        submitted = st.form_submit_button("✨ Orchestrate Agents")

with col2:
    if submitted:
        if not title or not goals:
            st.error("Please provide both a Title and Goals to start the orchestration.")
        else:
            # ── Live agent log ─────────────────────────────────────────────────
            log_box  = st.empty()
            prog_bar = st.progress(0, text="Initialising agents…")
            logs: list[str] = [
                "⚡ Axon Autonomous Pipeline starting…",
                f"📋 Project: {title}",
                "━" * 48,
                "🤖 [1/7] Context Reader  – extracting structured context…",
            ]

            def refresh_log():
                log_box.markdown(
                    f'<div class="agent-log">{"<br>".join(logs)}</div>',
                    unsafe_allow_html=True,
                )

            refresh_log()
            graph = build_graph()

            with st.spinner("🤖 Autonomous agents collaborating…"):
                result = graph.invoke({
                    "title":    title,
                    "goals":    goals,
                    "feedback": feedback,
                })

            # ── Post-run log enrichment ────────────────────────────────────────
            retries = result.get("retry_count", 0) - 1   # reviewer increments, so -1 for display
            review  = result.get("review_result", "")
            approved = "APPROVED" in review.upper()

            logs += [
                "🤖 [2/7] Vision Agent     – generating strategic purpose…",
            ]
            if retries > 0:
                critique_snip = result.get("critique", "")[:80]
                logs.append(f'  <span class="chip-rejected">REJECTED x{retries}</span>  Critique: {critique_snip}…')
                logs.append(f"🔄 Agents self-corrected {retries}x based on QA reviewer critique.")
            logs += [
                "🤖 [3/7] Flow Planner     – building execution roadmap…",
                f'🤖 [4/7] QA Reviewer      – {"<span class=\"chip-approved\">APPROVED</span>" if approved else "<span class=\"chip-rejected\">REJECTED (max retries)</span>"}',
                "🤖 [5/7] Diagram Agent    – generating Mermaid flowchart…",
                "🤖 [6/7] Risk Analyst     – stress-testing the plan…",
                "🤖 [7/7] Market Intel     – RAG web search + analysis…",
                "━" * 48,
                "✅ Full orchestration complete!",
            ]
            refresh_log()
            prog_bar.progress(100, text="Done!")

            st.success("🎉 Autonomous orchestration complete — all 7 agents finished!")

            # ── Agent decision summary ─────────────────────────────────────────
            m1, m2, m3 = st.columns(3)
            m1.metric("Self-Correction Retries", retries)
            m2.metric("Reviewer Verdict", "✅ Approved" if approved else "⚠️ Max Retries")
            m3.metric("Market Data Source", "Live RAG" if result.get("market_insights") else "Fallback")

            st.divider()

            # ── Output tabs ────────────────────────────────────────────────────
            tab1, tab2, tab3, tab4, tab5 = st.tabs([
                "🎯 Strategic Vision",
                "🪜 Execution Roadmap",
                "📊 Architecture Diagram",
                "🧠 Risk & Expert Critique",
                "🌍 Market Intelligence",
            ])

            with tab1:
                st.markdown(result.get("purpose", "_No output generated._"))

            with tab2:
                st.markdown(result.get("flow", "_No output generated._"))

            with tab3:
                diag = result.get("diagram", "").strip()
                # Strip stray fences
                for fence in ["```mermaid", "```"]:
                    diag = diag.replace(fence, "")
                diag = diag.strip()
                if diag:
                    st.markdown(f"```mermaid\n{diag}\n```")
                else:
                    st.info("No diagram generated.")

            with tab4:
                st.markdown(result.get("feedback_out", "_No output generated._"))

            with tab5:
                st.markdown(result.get("market_insights", "_No output generated._"))

            # ── PDF Export ─────────────────────────────────────────────────────
            st.divider()
            col_a, col_b = st.columns([1, 1])
            with col_a:
                try:
                    pdf_filename = "AI_Strategic_Plan.pdf"
                    exporter = PDFExporter(result)
                    exporter.export(pdf_filename)

                    with open(pdf_filename, "rb") as f:
                        b64 = base64.b64encode(f.read()).decode("utf-8")

                    st.markdown(
                        f'<a href="data:application/pdf;base64,{b64}" download="{pdf_filename}" style="text-decoration:none;">'
                        '<div style="background:linear-gradient(90deg,#0ea5e9,#2563eb);color:white;padding:12px;'
                        'border-radius:10px;text-align:center;font-weight:bold;">📥 Download PDF Strategic Report</div>'
                        '</a>',
                        unsafe_allow_html=True,
                    )
                except Exception as e:
                    st.error(f"PDF export failed: {e}")

            with col_b:
                st.info(
                    "💡 **Tip:** Click **Clear Agent Cache** in the sidebar whenever you change "
                    "your goals significantly — this forces agents to generate fresh perspectives "
                    "instead of serving cached results."
                )

    else:
        st.info("👈 Fill out the project details and click **Orchestrate Agents** to begin.")
        st.markdown("""
        <div class="card">
        <h4 style="color:#38bdf8">How it works</h4>
        <p style="color:#94a3b8;font-size:0.9rem;">
        Axon runs 7 specialised AI agents autonomously via a LangGraph state machine:<br><br>
        <b>1. Context Reader</b> – extracts structured context from your input<br>
        <b>2. Vision Agent</b> – writes a strategic project purpose<br>
        <b>3. Flow Planner</b> – builds a 8-12 step execution roadmap<br>
        <b>4. QA Reviewer</b> – critiques the plan; rejects &amp; loops if quality is low<br>
        <b>5. Diagram Agent</b> – converts the flow to a Mermaid architecture diagram<br>
        <b>6. Risk Analyst</b> – stress-tests for gaps, risks, and optimisations<br>
        <b>7. Market Intel</b> – RAG-powered web search for competitive analysis<br>
        </p>
        </div>
        """, unsafe_allow_html=True)
