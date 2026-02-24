from langgraph.graph import StateGraph
from pipeline_nodes import (
    context_node,
    purpose_node,
    flow_node,
    diagram_node,
    feedback_node,
    market_feedback_node,
    reviewer_node
)

# Define the state schema (keys passed between nodes)
class AgenticState(dict):
    title: str
    goals: str
    feedback: str
    context: str
    purpose: str
    flow: str
    diagram: str
    feedback_out: str
    market_insights: str
    review_result: str
    retry_count: int

def decide_next_step(state):
    """Conditional edge logic for self-correction."""
    review = state.get("review_result", "")
    retries = state.get("retry_count", 0)
    
    if "APPROVED" in review.upper() or retries >= 2:
        return "approved"
    return "rejected"

# Build LangGraph pipeline
def build_graph():
    builder = StateGraph(state_schema=AgenticState)

    # ✅ Add nodes
    builder.add_node("context_node", context_node)
    builder.add_node("purpose_node", purpose_node)
    builder.add_node("flow_node", flow_node)
    builder.add_node("reviewer_node", reviewer_node)
    builder.add_node("diagram_node", diagram_node)
    builder.add_node("feedback_node", feedback_node)
    builder.add_node("insights_node", market_feedback_node)

    # ✅ Linear flow for core logic
    builder.set_entry_point("context_node")
    builder.add_edge("context_node", "purpose_node")
    builder.add_edge("purpose_node", "flow_node")
    builder.add_edge("flow_node", "reviewer_node")

    # ✅ Conditional branching based on Review
    builder.add_conditional_edges(
        "reviewer_node",
        decide_next_step,
        {
            "rejected": "purpose_node", # Loop back for better results
            "approved": "diagram_node"  # Move to finalizing outputs
        }
    )

    # ✅ Parallel completion (Diagram, Feedback, and Insights can be parallel theoretically, 
    # but LangGraph StateGraph handles them sequentially here. For true parallel, we'd use fan-out)
    builder.add_edge("diagram_node", "feedback_node")
    builder.add_edge("feedback_node", "insights_node")
    builder.set_finish_point("insights_node")

    return builder.compile()
