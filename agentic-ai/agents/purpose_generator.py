import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

def generate_purpose(context):
    prompt = f"""
    Given this context: "{context}", generate a clear project purpose statement for a student academic project.
    """
    response = model.generate_content(prompt)
    return response.text.strip()
