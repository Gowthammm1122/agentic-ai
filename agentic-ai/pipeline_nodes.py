"""
Pipeline Node Wrappers
──────────────────────
Each function is a LangGraph node: receives the full AgenticState dict
and returns a partial dict of keys to update.

Key agentic behaviour here:
- purpose_node and flow_node receive the `critique` from a rejected review
  so agents can self-correct on the next loop pass.
- reviewer_node extracts the critique text and writes it into state so the
  above agents pick it up automatically.
"""

from agents.context_reader      import context_reader
from agents.purpose_generator   import generate_purpose
from agents.flow_planner        import plan_flow
from agents.diagram_generator   import generate_diagram
from agents.feedback_agent      import generate_feedback
from agents.market_feedback_agent import market_feedback_agent
from agents.reviewer_agent      import review_plan
from utils.cache                import agent_cache


# ── Context ────────────────────────────────────────────────────────────────────
@agent_cache
def context_node(state: dict) -> dict:
    print("  [Agent] Context Reader running…")
    return {
        "context":     context_reader(
                           state.get("title", ""),
                           state.get("goals", ""),
                           state.get("feedback", ""),
                       ),
        "retry_count": 0,
        "critique":    "",
    }


# ── Purpose ────────────────────────────────────────────────────────────────────
@agent_cache
def purpose_node(state: dict) -> dict:
    critique = state.get("critique", "")
    retry    = state.get("retry_count", 0)
    if retry > 0:
        print(f"  [Agent] Purpose Generator (retry {retry}, applying critique)…")
    else:
        print("  [Agent] Purpose Generator running…")

    return {
        "purpose": generate_purpose(
                       context=state.get("context", ""),
                       title=state.get("title", ""),
                       critique=critique,
                   )
    }


# ── Flow ───────────────────────────────────────────────────────────────────────
@agent_cache
def flow_node(state: dict) -> dict:
    critique = state.get("critique", "")
    retry    = state.get("retry_count", 0)
    if retry > 0:
        print(f"  [Agent] Flow Planner (retry {retry}, applying critique)…")
    else:
        print("  [Agent] Flow Planner running…")

    return {
        "flow": plan_flow(
                    purpose=state.get("purpose", ""),
                    context=state.get("context", ""),
                    critique=critique,
                )
    }


# ── Reviewer ───────────────────────────────────────────────────────────────────
def reviewer_node(state: dict) -> dict:
    """Not cached — must always run fresh to detect loop conditions."""
    print("  [Agent] Quality Reviewer running…")
    review = review_plan(
        context=state.get("context", ""),
        purpose=state.get("purpose", ""),
        flow=state.get("flow", ""),
    )

    # Extract critique text for downstream agents
    critique = ""
    if "REJECTED" in review.upper():
        # Strip the "REJECTED:" prefix and pass the rest as actionable critique
        parts = review.split(":", 1)
        critique = parts[1].strip() if len(parts) > 1 else review

    print(f"  [Reviewer] Verdict: {'APPROVED' if 'APPROVED' in review.upper() else 'REJECTED'}")

    return {
        "review_result": review,
        "critique":      critique,
        "retry_count":   state.get("retry_count", 0) + 1,
    }


# ── Diagram ────────────────────────────────────────────────────────────────────
@agent_cache
def diagram_node(state: dict) -> dict:
    print("  [Agent] Diagram Generator running…")
    return {"diagram": generate_diagram(state.get("flow", ""))}


# ── Risk / Feedback ────────────────────────────────────────────────────────────
@agent_cache
def feedback_node(state: dict) -> dict:
    print("  [Agent] Technical Analyst running…")
    return {
        "feedback_out": generate_feedback(
                            context=state.get("context", ""),
                            purpose=state.get("purpose", ""),
                            flow=state.get("flow", ""),
                        )
    }


# ── Market Intelligence ────────────────────────────────────────────────────────
@agent_cache
def market_feedback_node(state: dict) -> dict:
    print("  [Agent] Market Intelligence Agent running…")
    return {
        "market_insights": market_feedback_agent(
                               context=state.get("context", ""),
                               purpose=state.get("purpose", ""),
                               flow=state.get("flow", ""),
                           )
    }
