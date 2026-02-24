from utils.llm import safe_generate_content

def context_reader(title, goals, feedback):
    prompt = f"""
    Title: {title}
    Goals: {goals}
    Feedback Notes: {feedback}

    Based on this input, extract the context or background the user is working with.
    """
    return safe_generate_content(prompt)

