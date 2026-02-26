# Agentic AI Planner — Project Overview

## What It Does
A **multi-agent AI system** that automatically generates complete project plans from a simple title, goals, and requirements. It outputs strategic reports with execution roadmaps, architecture diagrams, risk assessments, and market analysis — all in under 45 seconds.

---

## How It Works

The system chains **7 specialized AI agents** in a pipeline (built on **LangGraph**), each handling one part of the planning process:

| # | Agent | Role |
|---|-------|------|
| A1 | **Context Reader** | Parses and structures user input (title, goals, requirements) |
| A2 | **Strategic Vision** | Generates a high-level purpose and vision statement |
| A3 | **Execution Architect** | Creates a step-by-step execution flow aligned with the vision |
| A4 | **Reviewer Critic** | Evaluates the plan for alignment, depth, and actionability |
| A5 | **Diagram Generator** | Converts the execution flow into a Mermaid.js architecture diagram |
| A6 | **Senior Technical Analyst** | Provides risk assessment, identifies gaps and optimizations |
| A7 | **Market Intelligence** | Fetches real-time web data via RAG to ground the market analysis |

### Pipeline Flow
```
User Input → Context Reader → Strategic Vision → Execution Architect
                                                        ↓
                                                  Reviewer Critic
                                                   ↙        ↘
                                             REJECTED      APPROVED
                                           (loop back        ↓
                                            to A2)    Diagram Generator
                                                        ↓
                                                  Tech Analyst
                                                        ↓
                                                  Market Intel
                                                        ↓
                                                  Final Report + PDF
```

---

## Key Features

- **Self-Correction Loop**: The Reviewer Critic can reject a plan and send it back for re-generation (up to 2 retries), improving 72% of initially rejected plans.
- **RAG-Powered Market Analysis**: The Market Intelligence agent searches the web (Serper API), embeds results in ChromaDB, and uses vector similarity to ground analysis in real data.
- **Deterministic Caching**: SHA-256 content-addressed cache ensures reproducibility and saves API costs. The Reviewer Critic is excluded from caching to keep evaluations dynamic.
- **Fault-Tolerant LLM Calls**: Exponential backoff on rate limits, automatic model fallback (primary → backup), and graceful error handling.
- **PDF Export**: One-click generation of publication-ready reports via FPDF2.

---

## Tech Stack

| Component | Technology |
|-----------|------------|
| Orchestration | LangGraph (StateGraph) |
| LLM Backend | Groq API |
| Primary Model | GPT-OSS-120B |
| Fallback Model | LLaMA-3.3-70B |
| Embeddings | Google Gemini Embedding 001 |
| Vector Store | ChromaDB |
| Web Search | Serper API |
| Frontend | Streamlit |
| PDF Export | FPDF2 |

---

## Evaluation Results (50 scenarios, 5 domains)

| Method | Overall Quality (1–5) |
|--------|----------------------|
| Single-Shot LLM | 3.08 |
| Chain-of-Thought | 3.42 |
| Multi-Agent (no self-correction) | 3.74 |
| **Full Pipeline (ours)** | **4.12** |

- **33.8% improvement** over single-shot baselines.
- **10.2% improvement** from the self-correction loop alone.
- Only 28% of plans passed on the first attempt — validating the need for the critic agent.
- Average latency: **~39 seconds** per project plan.

---

## Project Structure

```
agentic-ai/
├── main.py                # Streamlit frontend
├── run_pipeline.py        # CLI entry point
├── pipeline_graph.py      # LangGraph DAG definition
├── pipeline_nodes.py      # Agent node implementations
├── export_to_pdf.py       # PDF report generation
├── agents/
│   ├── context_reader.py          # A1: Input parsing
│   ├── purpose_generator.py       # A2: Strategic vision
│   ├── flow_planner.py            # A3: Execution flow
│   ├── reviewer_agent.py          # A4: Self-correction critic
│   ├── diagram_generator.py       # A5: Mermaid diagrams
│   ├── feedback_agent.py          # A6: Technical analysis
│   └── market_feedback_agent.py   # A7: RAG market intelligence
├── utils/
│   ├── llm.py             # LLM wrapper with fallback
│   └── cache.py           # SHA-256 caching layer
├── chroma_db/             # Vector store data
└── journal/               # IEEE paper and references
```

---

## Limitations

- Quality is bounded by the underlying LLM's capability.
- Agents 5–7 run sequentially but could be parallelized (~30% latency savings).
- Single critic — a panel of diverse critics could improve corrections.
- Market agent requires internet access and a Serper API key.
