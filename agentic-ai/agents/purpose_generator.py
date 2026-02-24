from utils.llm import safe_generate_content

def generate_purpose(context, title):
    prompt = f"""
    You are the Strategic Vision Agent. 
    Project Title: {title}
    Full Context from Reader Agent: {context}

    Based on the above, generate a professional, high-level Project Purpose statement. 
    It should be visionary yet concrete.
    """
    return safe_generate_content(prompt)
