from utils.llm import safe_generate_content

def generate_feedback(context, purpose, flow):
    prompt = f"""
    You are the Senior Technical Analyst Agent. 
    Collaborators have produced the following plan:
    - Context: {context}
    - Vision/Purpose: {purpose}
    - Execution Flow: {flow}

    TASK: Provide a critical, expert-level feedback review. 
    Highlight:
    1. Potential Risks: What could go wrong in this execution?
    2. Missing Pieces: Is there a step missing in the flow?
    3. Technical Optimization: One way to make this more efficient.

    Use bullet points (*) for each feedback item to ensure the PDF report is structured and professional.
    """
    return safe_generate_content(prompt)
