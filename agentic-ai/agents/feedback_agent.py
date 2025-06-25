import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

def generate_feedback(context, purpose, flow):
    prompt = f"""
    Review the following:
    Context: {context}
    Purpose: {purpose}
    Flow: {flow}

    Provide concise and actionable feedback for improving the project plan.
    """
    response = model.generate_content(prompt)
    return response.text.strip()
