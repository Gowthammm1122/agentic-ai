from utils.llm import safe_generate_content

def plan_flow(purpose, context):
    prompt = f"""
    You are the Execution Architect Agent. 
    Collaborator (Vision Agent) defined this Purpose: "{purpose}"
    Additional Context: "{context}"

    Task: Break down this project into a clear, numbered step-by-step Execution Flow. 
    Ensure the steps are logical, technical, and actionable. 
    Use a numbered list format (1, 2, 3...) for clarity in the final report.
    """
    return safe_generate_content(prompt)
