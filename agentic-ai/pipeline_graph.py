"""
LangGraph Pipeline
──────────────────
Orchestrates 7 specialised agents as an autonomous, self-correcting workflow.

Flow:
  context_node
      ↓
  purpose_node  ←──────────────────────┐  (REJECTED loop)
      ↓                                │
  flow_node                            │
      ↓                                │
  reviewer_node ──[REJECTED]───────────┘
      │
  [APPROVED]
      ↓
  diagram_node → feedback_node → insights_node → END
"""

from typing import TypedDict, Optional
from langgraph.graph import StateGraph, END
from pipeline_nodes import (
    context_node,
    purpose_node,
    flow_node,
    reviewer_node,
    diagram_node,
    feedback_node,
    market_feedback_node,
)


# ── State schema ───────────────────────────────────────────────────────────────
class AgenticState(TypedDict, total=False):
    # ── Inputs from the user ──
    title:          str
    goals:          str
    feedback:       str

    # ── Agent outputs ──
    context:        str
    purpose:        str
    flow:           str
    diagram:        str
    feedback_out:   str
    market_insights: str

    # ── Self-correction control ──
    review_result:  str    # raw reviewer response ("APPROVED" or "REJECTED: …")
    critique:       str    # extracted critique text passed to agents on retry
    retry_count:    int


# ── Conditional routing ────────────────────────────────────────────────────────
def decide_next_step(state: AgenticState) -> str:
    """
    Route after reviewer:
      APPROVED  → proceed to diagram / finalisation
      REJECTED  → loop back to purpose_node (max 2 retries)
    """
    review    = state.get("review_result", "")
    retries   = state.get("retry_count", 0)

    if "APPROVED" in review.upper() or retries >= 2:
        return "approved"

    return "rejected"


# ── Graph builder ──────────────────────────────────────────────────────────────
def build_graph():
    builder = StateGraph(AgenticState)

    # Register nodes
    builder.add_node("context_node",   context_node)
    builder.add_node("purpose_node",   purpose_node)
    builder.add_node("flow_node",      flow_node)
    builder.add_node("reviewer_node",  reviewer_node)
    builder.add_node("diagram_node",   diagram_node)
    builder.add_node("feedback_node",  feedback_node)
    builder.add_node("insights_node",  market_feedback_node)

    # Core linear path
    builder.set_entry_point("context_node")
    builder.add_edge("context_node", "purpose_node")
    builder.add_edge("purpose_node", "flow_node")
    builder.add_edge("flow_node",    "reviewer_node")

    # Self-correction conditional branch
    builder.add_conditional_edges(
        "reviewer_node",
        decide_next_step,
        {
            "rejected": "purpose_node",   # loop: re-plan with critique
            "approved": "diagram_node",   # proceed to finalisation
        },
    )

    # Finalisation chain
    builder.add_edge("diagram_node",  "feedback_node")
    builder.add_edge("feedback_node", "insights_node")
    builder.add_edge("insights_node", END)

    return builder.compile()
