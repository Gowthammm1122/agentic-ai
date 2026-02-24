from agents.context_reader import context_reader
from agents.purpose_generator import generate_purpose
from agents.flow_planner import plan_flow
from agents.diagram_generator import generate_diagram
from agents.feedback_agent import generate_feedback
from agents.market_feedback_agent import market_feedback_agent
from agents.reviewer_agent import review_plan
from utils.cache import agent_cache

@agent_cache
def context_node(state):
    return {
        "context": context_reader(state["title"], state["goals"], state["feedback"]),
        "retry_count": 0
    }

@agent_cache
def purpose_node(state):
    return {"purpose": generate_purpose(state["context"], state["title"])}

@agent_cache
def flow_node(state):
    # Flow planner now sees both context and purpose for better alignment
    return {"flow": plan_flow(state["purpose"], state["context"])}

@agent_cache
def diagram_node(state):
    return {"diagram": generate_diagram(state["flow"])}

@agent_cache
def feedback_node(state):
    return {"feedback_out": generate_feedback(state["context"], state["purpose"], state["flow"])}

@agent_cache
def market_feedback_node(state):
    # Market agent sees the full scope
    return {"market_insights": market_feedback_agent(state["context"], state["purpose"], state["flow"])}

def reviewer_node(state):
    # We don't cache the reviewer because it needs to be dynamic to detect loops
    review_result = review_plan(state["context"], state["purpose"], state["flow"])
    return {
        "review_result": review_result,
        "retry_count": state.get("retry_count", 0) + 1
    }
