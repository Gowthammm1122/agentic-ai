from utils.llm import safe_generate_content

def generate_diagram(flow_steps):
    prompt = f"""
    Create a simple Mermaid-style flowchart for the following process:
    {flow_steps}

    Use only Mermaid flowchart syntax, no explanation.
    """
    return safe_generate_content(prompt)
