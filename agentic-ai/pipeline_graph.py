from langgraph.graph import StateGraph
from pipeline_nodes import (
    context_node,
    purpose_node,
    flow_node,
    diagram_node,
    feedback_node,
    market_feedback_node
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

# Build LangGraph pipeline
def build_graph():
    builder = StateGraph(state_schema=AgenticState)

    # ✅ Node names must NOT match state keys
    builder.add_node("context_node", context_node)
    builder.add_node("purpose_node", purpose_node)
    builder.add_node("flow_node", flow_node)
    builder.add_node("diagram_node", diagram_node)
    builder.add_node("feedback_node", feedback_node)
    builder.add_node("insights_node", market_feedback_node)

    builder.set_entry_point("context_node")
    builder.add_edge("context_node", "purpose_node")
    builder.add_edge("purpose_node", "flow_node")
    builder.add_edge("flow_node", "diagram_node")
    builder.add_edge("diagram_node", "feedback_node")
    builder.add_edge("feedback_node", "insights_node")
    builder.set_finish_point("insights_node")

    return builder.compile()
