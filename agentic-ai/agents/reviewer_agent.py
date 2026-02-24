from utils.llm import safe_generate_content

def review_plan(context, purpose, flow):
    prompt = f"""
    You are an Agentic Critic. Your job is to ensure the project plan is high-quality, actionable, and aligns with the user's goals.

    Project Context: {context}
    Generated Purpose: {purpose}
    Generated Flow: {flow}

    Analyze the plan for:
    1. Alignment: Does the flow actually achieve the goals?
    2. Depth: Is the purpose too generic?
    3. Actionability: Are the flow steps clear?

    If the plan is good, respond with exactly: "APPROVED".
    If the plan needs improvement, respond with constructive feedback starting with "REJECTED: [your feedback here]".
    """
    return safe_generate_content(prompt)
