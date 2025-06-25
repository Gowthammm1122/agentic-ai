import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

def plan_flow(purpose):
    prompt = f"""
    Break down this project purpose into a clear step-by-step workflow:
    "{purpose}"
    """
    response = model.generate_content(prompt)
    return response.text.strip()
