import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

def generate_diagram(flow_steps):
    prompt = f"""
    Create a simple Mermaid-style flowchart for the following process:
    {flow_steps}

    Use only Mermaid flowchart syntax, no explanation.
    """
    response = model.generate_content(prompt)
    return response.text.strip()
