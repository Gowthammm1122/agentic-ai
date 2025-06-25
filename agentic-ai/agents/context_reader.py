import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

def context_reader(title, goals, feedback):
    prompt = f"""
    Title: {title}
    Goals: {goals}
    Feedback Notes: {feedback}

    Based on this input, extract the context or background the user is working with.
    """
    response = model.generate_content(prompt)
    return response.text.strip()

